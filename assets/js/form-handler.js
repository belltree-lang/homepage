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
      //    自由記述の欄名がフォームごとに違う（お問い合わせ内容・応募動機・備考）ため、
      //    氏名と textarea を全部つないで見る。
      const jaSource = [form.querySelector('[name="氏名"]')]
        .concat(Array.from(form.querySelectorAll('textarea')))
        .map(el => (el && el.value) || '')
        .join('');
      if (jaSource && !/[ぁ-んァ-ヶー一-龥]/.test(jaSource)) {
        showNotice('恐れ入りますが、お名前とご入力内容は日本語でご記入ください。'
                 + 'お急ぎの場合や日本語での入力が難しい場合は、042-682-2839 へお電話ください。');
        restoreBtn();
        return;
      }

      const formData = new FormData(form);
      const formType = form.getAttribute('data-form-type');
      formData.append('formType', formType);

      try {
        // ページを通った送信であることの印。印の無い送信は GAS 側で台帳から外す
        const stamp = await belltreeSignSubmission(formType);
        formData.append('__ts', stamp.ts);
        formData.append('__sig', stamp.sig);
        const urlEncodedData = new URLSearchParams(formData).toString();

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
