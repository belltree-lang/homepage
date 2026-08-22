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
    // bot は開いた直後に送信してくる。人は入力に時間がかかる。
    const formOpenedAt = Date.now();
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

      // ---- bot よけ ----
      const restoreBtn = () => {
        submitBtn.innerText = originalText;
        submitBtn.disabled = false;
      };
      const showNotice = (msg) => {
        let n = form.querySelector('.form-notice');
        if (!n) {
          n = document.createElement('p');
          n.className = 'form-notice';
          n.style.cssText = 'color:#b45309;margin-top:1rem;line-height:1.8;';
          form.appendChild(n);
        }
        n.innerText = msg;
      };

      // ① 見えない欄に入力があれば bot（人には見えない位置にある）
      const honeypot = form.querySelector('input[name="url_website_hp"]');
      if (honeypot && honeypot.value !== "") {
        console.warn("Spam detected: honeypot");
        restoreBtn();
        return; // 静かに落とす
      }

      // ② 開いてから数秒で送信されたら bot（人の入力速度ではありえない）
      if (Date.now() - formOpenedAt < 6000) {
        console.warn("Spam detected: too fast");
        restoreBtn();
        return; // 静かに落とす
      }

      // ③ 日本語が1文字も無ければ、機械が英字を流し込んだ疑いが濃い。
      //    ただし本当に日本語が書けない方もいるため、静かに捨てず電話をご案内する。
      const jaSource = [
        form.querySelector('[name="お名前"]'),
        form.querySelector('[name="ご相談内容"]')
      ].map(el => (el && el.value) || '').join('');
      if (jaSource && !/[ぁ-んァ-ヶー一-龥]/.test(jaSource)) {
        showNotice('恐れ入りますが、お名前とご相談内容は日本語でご記入ください。'
                 + 'お急ぎの場合や日本語での入力が難しい場合は、042-682-2839 へお電話ください。');
        restoreBtn();
        return;
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
        
        // 計測: 実際に送信できたときだけ「問い合わせ1件」として数える
        // （ページ側の submit 監視だと、bot の送信試行や中断も1件に数えてしまう）
        if (window.gtag) {
          gtag('event', 'generate_lead', {
            method: 'form',
            page: form.getAttribute('data-form-type') || 'form'
          });
        }

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
