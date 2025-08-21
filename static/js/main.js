// PDF to LaTeX Converter - JavaScript

// Global variables
let selectedFile = null;
let currentStep = 1;

// DOM loaded event
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    const pdfFileInput = document.getElementById('pdfFile');
    const uploadArea = document.getElementById('uploadArea');
    
    // File input change event
    pdfFileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop events
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('click', () => pdfFileInput.click());
}

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        validateAndDisplayFile(file);
    }
}

// Handle drag over
function handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.classList.add('dragover');
}

// Handle drag leave
function handleDragLeave(event) {
    event.currentTarget.classList.remove('dragover');
}

// Handle file drop
function handleDrop(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        validateAndDisplayFile(files[0]);
    }
}

// Validate and display selected file
function validateAndDisplayFile(file) {
    // Validate file type
    if (!file.type.includes('pdf')) {
        showError('Please select a PDF file.');
        return;
    }
    
    // Validate file size (10MB = 10485760 bytes)
    const maxSize = 10485760;
    if (file.size > maxSize) {
        showError(`File is too large. Maximum size is ${(maxSize / 1024 / 1024).toFixed(1)}MB.`);
        return;
    }
    
    // File is valid
    selectedFile = file;
    displayFileInfo(file);
}

// Display file information
function displayFileInfo(file) {
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const fileInfo = document.getElementById('fileInfo');
    const uploadArea = document.getElementById('uploadArea');
    
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    
    uploadArea.style.display = 'none';
    fileInfo.style.display = 'block';
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Clear selected file
function clearFile() {
    selectedFile = null;
    document.getElementById('pdfFile').value = '';
    document.getElementById('uploadArea').style.display = 'block';
    document.getElementById('fileInfo').style.display = 'none';
    hideAllSections();
}

// Convert PDF to LaTeX
async function convertPDF() {
    if (!selectedFile) {
        showError('Please select a PDF file first.');
        return;
    }
    
    // Show loading animation
    showLoading();
    startLoadingSteps();
    
    // Prepare form data
    const formData = new FormData();
    formData.append('pdf_file', selectedFile);
    
    try {
        // Make API request
        const response = await fetch('/convert', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            // Success - show results
            stopLoadingSteps();
            showResults(result.latex_code);
        } else if (response.status === 429) {
            // Rate limit exceeded - special handling
            const retryAfter = response.headers.get('Retry-After');
            const limitType = result.limit_type || 'general';
            
            let message = result.message || 'Rate limit exceeded. Please try again later.';
            
            if (limitType === 'convert') {
                // Daily conversion limit hit
                message = result.message + '\n\nRate limit resets at midnight UTC.';
            } else if (retryAfter) {
                message += `\n\nYou can try again in ${retryAfter} seconds.`;
            }
            
            throw new Error(message);
        } else {
            // Other errors from server
            throw new Error(result.error || 'Unknown error occurred');
        }
        
    } catch (error) {
        stopLoadingSteps();
        showError(`Conversion failed: ${error.message}`);
        console.error('Conversion error:', error);
    }
}

// Show loading animation
function showLoading() {
    hideAllSections();
    document.getElementById('loading').style.display = 'block';
}

// Start loading steps animation
function startLoadingSteps() {
    currentStep = 1;
    updateLoadingStep();
    
    // Simulate progress through steps
    setTimeout(() => {
        currentStep = 2;
        updateLoadingStep();
    }, 2000);
    
    setTimeout(() => {
        currentStep = 3;
        updateLoadingStep();
    }, 4000);
}

// Update loading step
function updateLoadingStep() {
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
        if (index < currentStep) {
            step.classList.add('active');
        } else {
            step.classList.remove('active');
        }
    });
}

// Stop loading steps
function stopLoadingSteps() {
    currentStep = 1;
    const steps = document.querySelectorAll('.step');
    steps.forEach(step => step.classList.remove('active'));
}

// Show results
function showResults(latexCode) {
    hideAllSections();
    
    const resultSection = document.getElementById('resultSection');
    const latexOutput = document.getElementById('latexOutput');
    
    latexOutput.textContent = latexCode;
    resultSection.style.display = 'block';
    
    // Scroll to results
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

// Show error
function showError(message) {
    hideAllSections();
    
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    
    // Scroll to error
    errorSection.scrollIntoView({ behavior: 'smooth' });
}

// Hide all result sections
function hideAllSections() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
}

// Copy to clipboard
async function copyToClipboard() {
    const latexCode = document.getElementById('latexOutput').textContent;
    
    try {
        await navigator.clipboard.writeText(latexCode);
        
        // Show feedback
        const button = event.target;
        const originalText = button.innerHTML;
        button.innerHTML = '✅ Copied!';
        button.style.background = 'linear-gradient(45deg, #2ecc71, #27ae60)';
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.style.background = '';
        }, 2000);
        
    } catch (err) {
        console.error('Failed to copy: ', err);
        
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = latexCode;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        
        showError('Copied to clipboard!');
    }
}

// Download LaTeX file
function downloadLatex() {
    const latexCode = document.getElementById('latexOutput').textContent;
    const fileName = selectedFile ? selectedFile.name.replace('.pdf', '.tex') : 'converted.tex';
    
    // Create blob and download
    const blob = new Blob([latexCode], { type: 'text/plain;charset=utf-8' });
    const url = window.URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    a.style.display = 'none';
    
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    window.URL.revokeObjectURL(url);
    
    // Show feedback
    const button = event.target;
    const originalText = button.innerHTML;
    button.innerHTML = '✅ Downloaded!';
    button.style.background = 'linear-gradient(45deg, #2ecc71, #27ae60)';
    
    setTimeout(() => {
        button.innerHTML = originalText;
        button.style.background = '';
    }, 2000);
}

// Clear results and start over
function clearResults() {
    clearFile();
    hideAllSections();
}

// Utility function to show notifications
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#e74c3c' : '#2ecc71'};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        font-weight: 500;
        max-width: 300px;
        word-wrap: break-word;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}
