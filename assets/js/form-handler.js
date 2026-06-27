/**
 * BellTree Form Handler
 * Handles validation, anti-spam, and submission to Google Apps Script.
 */

const BELLTREE_FORM_CONFIG = {
  // Configurable placeholder for the Google Apps Script Web App URL
  gasEndpoint: "https://script.google.com/macros/s/AKfycbxGscrnn3F6USh7baej3inWP0WYREab4DrU3779tfn1TVYH3QRYj7McYLraF7QPDHAAtg/exec",
  adminEmail: "belltree@belltree1102.com"
};

document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('form[data-form-type]');
  
  if (forms.length === 0) return;

  forms.forEach(form => {
    const submitBtn = form.querySelector('button[type="submit"]');
    const privacyCheck = form.querySelector('input[name="privacy_agreement"]');
    
    // Initial State styling
    if (privacyCheck && submitBtn) {
      const toggleSubmit = () => {
        submitBtn.disabled = !privacyCheck.checked;
        if(submitBtn.disabled) {
          submitBtn.style.opacity = '0.5';
          submitBtn.style.cursor = 'not-allowed';
        } else {
          submitBtn.style.opacity = '1';
          submitBtn.style.cursor = 'pointer';
        }
      };
      privacyCheck.addEventListener('change', toggleSubmit);
      toggleSubmit(); // run once
    }

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const originalText = submitBtn.innerText;
      submitBtn.innerText = '送信中...';
      submitBtn.disabled = true;

      // Anti-spam basic honeypot check (if added to forms)
      const honeypot = form.querySelector('input[name="url_website_hp"]');
      if (honeypot && honeypot.value !== "") {
        console.warn("Spam detected");
        return; // silently fail for bots
      }

      const formData = new FormData(form);
      formData.append('formType', form.getAttribute('data-form-type'));
      const urlEncodedData = new URLSearchParams(formData).toString();

      try {
        // Use application/x-www-form-urlencoded to integrate with GAS doPost parameters natively
        const response = await fetch(BELLTREE_FORM_CONFIG.gasEndpoint, {
          method: 'POST',
          mode: 'no-cors',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: urlEncodedData
        });
        
        // no-cors returns opaque response, assume success if no network error
        // GA4 conversion: フォーム送信をリードとして計測（sendBeaconで遷移後も送信される）
        if (typeof gtag === 'function') {
          gtag('event', 'generate_lead', { form_type: form.getAttribute('data-form-type') || 'inquiries' });
        }
        const redirectUrl = form.getAttribute('data-redirect-url') || './thanks/index.html';
        window.location.href = redirectUrl;

      } catch (err) {
        console.error('Form submission error:', err);
        const errorMsg = document.createElement('p');
        errorMsg.style.color = '#e74c3c';
        errorMsg.style.marginTop = '1rem';
        errorMsg.innerText = '送信に失敗しました。通信環境をご確認のうえ、再度お試しください。';
        form.appendChild(errorMsg);
        
        submitBtn.innerText = originalText;
        submitBtn.disabled = false;
      }
    });
  });
});
