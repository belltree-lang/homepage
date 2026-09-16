/**
 * BellTree Form Handler
 * Handles validation, anti-spam, and submission to Google Apps Script.
 */

const BELLTREE_FORM_CONFIG = {
  // Configurable placeholder for the Google Apps Script Web App URL
  gasEndpoint: "https://script.google.com/macros/s/AKfycbxGscrnn3F6USh7baej3inWP0WYREab4DrU3779tfn1TVYH3QRYj7McYLraF7QPDHAAtg/exec",
  adminEmail: "belltree@belltree1102.com",
  // ページを通った送信であることの印を作るための合鍵。公開JSに載るので秘密ではない。
  // 目的は、ページを開かずに GAS の URL へ直接POSTしてくる送信を見分けること。
  formKey: "3f5c042d71f4d55dd5f7773c6c4f3be4"
};

// 送信のたびに「時刻:フォーム種別:合鍵」の SHA-256 を作って添える。
// GAS 側が同じ計算をして照合し、合わない送信は台帳から外す。
async function belltreeSignSubmission(formType) {
  const ts = String(Date.now());
  const msg = ts + ':' + (formType || '') + ':' + BELLTREE_FORM_CONFIG.formKey;
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(msg));
  const sig = Array.from(new Uint8Array(digest))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
  return { ts, sig };
}

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
      const formType = form.getAttribute('data-form-type');
      const dataPayload = Object.fromEntries(formData.entries());
      dataPayload.formType = formType;

      try {
        // ページを通った送信であることの印。印の無い送信は GAS 側で台帳から外す
        const stamp = await belltreeSignSubmission(formType);
        dataPayload.__ts = stamp.ts;
        dataPayload.__sig = stamp.sig;

        // We use text/plain to avoid CORS preflight issues with GAS
        const response = await fetch(BELLTREE_FORM_CONFIG.gasEndpoint, {
          method: 'POST',
          mode: 'no-cors',
          headers: {
            'Content-Type': 'text/plain'
          },
          body: JSON.stringify(dataPayload)
        });
        
        // no-cors returns opaque response, assume success if no network error
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
