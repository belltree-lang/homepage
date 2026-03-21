/**
 * Google Apps Script Web App for BellTree Forms
 * Handles 7 different form types, writes to appropriate sheets, and sends auto-replies.
 * 
 * SETUP INSTRUCTIONS:
 * 1. Create a new Google Spreadsheet.
 * 2. Create the following 7 sheet tabs EXACTLY:
 *    - inquiries
 *    - recruit_applications
 *    - fitness_trials
 *    - acupuncture_consultations
 *    - daycare_consultations
 *    - legal_consultations
 *    - partner_inquiries
 * 3. Go to Extensions -> Apps Script.
 * 4. Paste this code.
 * 5. Update the SPREADSHEET_ID below.
 * 6. Deploy -> New Deployment -> Web App (Execute as: Me, Who has access: Anyone).
 * 7. Copy the Web App URL and update BELLTREE_FORM_CONFIG in assets/js/form-handler.js.
 */

const CONFIG = {
  SPREADSHEET_ID: "PLACEHOLDER_SPREADSHEET_ID",
  ADMIN_EMAIL: "belltree@belltree1102.com",
  COMPANY_NAME: "株式会社べるつりー",
  COMPANY_PHONE: "042-682-2839",
  COMPANY_ADDRESS: "東京都八王子市下柚木3-7-2-401"
};

// Form mappings to their specific settings
const FORM_MAP = {
  "inquiries": {
    sheetName: "inquiries",
    prefix: "INQ",
    subject: "【株式会社べるつりー】お問い合わせを受け付けました",
    senderName: "株式会社べるつりー",
    columns: ["氏名", "メールアドレス", "電話番号", "会社名・団体名", "お問い合わせ種別", "お問い合わせ内容"]
  },
  "recruit_applications": {
    sheetName: "recruit_applications",
    prefix: "REC",
    subject: "【株式会社べるつりー 採用窓口】ご応募を受け付けました",
    senderName: "株式会社べるつりー 採用窓口",
    columns: ["氏名", "ふりがな", "メールアドレス", "電話番号", "年齢", "希望職種", "勤務希望条件", "応募動機・自由記述", "保有資格", "現在の勤務状況", "見学希望の有無"]
  },
  "fitness_trials": {
    sheetName: "fitness_trials",
    prefix: "FIT",
    subject: "【べるフィット】見学・体験のお申し込みを受け付けました",
    senderName: "べるフィット",
    columns: ["氏名", "メールアドレス", "電話番号", "希望内容", "希望日時", "年齢層", "健康上の配慮事項", "備考"]
  },
  "acupuncture_consultations": {
    sheetName: "acupuncture_consultations",
    prefix: "ACU",
    subject: "【べるつりー鍼灸マッサージ院】ご相談を受け付けました",
    senderName: "べるつりー鍼灸マッサージ院",
    columns: ["氏名", "メールアドレス", "電話番号", "ご本人との関係", "主な相談内容", "お悩みの部位・箇所", "訪問希望地域", "介護認定の有無", "医師・ケアマネの関与有無", "希望連絡方法", "備考"]
  },
  "daycare_consultations": {
    sheetName: "daycare_consultations",
    prefix: "DAY",
    subject: "【べるフィット】通所リハ・介護相談を受け付けました",
    senderName: "べるフィット",
    columns: ["氏名", "メールアドレス", "電話番号", "ご本人との関係", "現在の困りごと", "利用希望者の年齢層", "要支援・要介護認定の有無", "ケアマネ有無", "見学希望日時", "備考"]
  },
  "legal_consultations": {
    sheetName: "legal_consultations",
    prefix: "LEG",
    subject: "【べるリーガル行政書士事務所】ご相談を受け付けました",
    senderName: "べるリーガル行政書士事務所",
    columns: ["氏名", "メールアドレス", "電話番号", "相談種別", "相談内容", "年齢層", "面談希望方法", "希望日時", "備考"]
  },
  "partner_inquiries": {
    sheetName: "partner_inquiries",
    prefix: "PAR",
    subject: "【株式会社べるつりー 地域連携窓口】お問い合わせを受け付けました",
    senderName: "株式会社べるつりー 地域連携窓口",
    columns: ["氏名", "所属先", "メールアドレス", "電話番号", "問い合わせ種別", "問い合わせ内容", "備考"]
  }
};

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const formType = data.formType;
    
    if (!FORM_MAP[formType]) {
      throw new Error("Invalid formType: " + formType);
    }
    
    const settings = FORM_MAP[formType];
    const timestamp = new Date();
    
    // Process Spreadsheet Writing
    const sheet = SpreadsheetApp.openById(CONFIG.SPREADSHEET_ID).getSheetByName(settings.sheetName);
    if (!sheet) throw new Error("Sheet not found: " + settings.sheetName);
    
    // Generate ID
    const dateStr = Utilities.formatDate(timestamp, "JST", "yyyyMMdd");
    const lastRow = Math.max(sheet.getLastRow(), 1);
    const sequenceObj = Utilities.formatString("%04d", lastRow); 
    const recordId = `${settings.prefix}-${dateStr}-${sequenceObj}`;
    
    // Prepare standard specific row data
    // Format: 受付日時, フォーム種別, 受付番号, 対応状況, 対応担当者, 最終対応日, 備考, <Form Specific Columns>, 個人情報同意, 自動返信送信状況, 管理者通知送信状況
    let rowData = [
      timestamp, 
      formType, 
      recordId, 
      "未対応", 
      "", 
      "", 
      ""
    ];
    
    settings.columns.forEach(col => {
      // mapping name attributes to columns
      // For simplicity, we assume HTML form inputs have name attributes that exactly match the Japanese column names, 
      // or we do mapping here. Assuming frontend form inputs use english names mapped below, or we just extract 
      // what matches exactly. Let's extract from the data payload by key.
      const val = data[col] || data[getEnglishKey(col)] || "";
      rowData.push(val);
    });
    
    const privacyAgreement = data.privacy_agreement || data["個人情報同意チェック"] ? "同意済" : "未同意";
    rowData.push(privacyAgreement);
    rowData.push("未送信"); // Auto-reply status pos
    rowData.push("未送信"); // Admin notify status pos
    
    // Append to sheet
    sheet.appendRow(rowData);
    const newRowIndex = sheet.getLastRow();
    
    // Send Emails
    let autoReplyStatus = "失敗";
    let adminNotifyStatus = "失敗";
    
    const userEmail = data.email || data["メールアドレス"] || data["メールアドレス_必須"];
    
    // 1. Admin Notification
    try {
      const adminBody = `Webサイトから新しいフォーム送信がありました。\n\n`
        + `◆受付番号: ${recordId}\n`
        + `◆フォーム種別: ${formType}\n\n`
        + `確認はスプレッドシート（${settings.sheetName}シート）より行ってください。\n`;
      
      MailApp.sendEmail({
        to: CONFIG.ADMIN_EMAIL,
        subject: `【Web通知】${recordId} 新規お問い合わせ`,
        body: adminBody,
        name: "BellTree System"
      });
      adminNotifyStatus = "送信済";
    } catch(err) {
      console.error("Admin Email Error: " + err);
    }
    
    // 2. Auto-reply
    if (userEmail) {
      try {
        let extraText = "内容を確認のうえ、通常2営業日以内を目安にご連絡いたします。\n";
        if (formType === "recruit_applications") {
          extraText = "書類提出や見学調整が必要な場合は、改めてご案内いたします。\n";
        } else if (formType === "partner_inquiries") {
          extraText = "内容を確認のうえ、担当者よりご連絡いたします。\n";
        }
        
        const autoReplyBody = `${data.name || data["氏名"] || ""} 様\n\n`
          + `送信が完了しました。\n`
          + extraText + `\n`
          + `このメールは自動返信です。本メールに心当たりがない場合は破棄してください。\n\n`
          + `------------------------\n`
          + `${CONFIG.COMPANY_NAME}\n`
          + `${CONFIG.COMPANY_ADDRESS}\n`
          + `メール：${CONFIG.ADMIN_EMAIL}\n`
          + `電話：${CONFIG.COMPANY_PHONE}\n`
          + `受付時間：9:00〜18:00\n`
          + `------------------------`;

        MailApp.sendEmail({
          to: userEmail,
          subject: settings.subject,
          body: autoReplyBody,
          name: settings.senderName
        });
        autoReplyStatus = "送信済";
      } catch(err) {
        console.error("User Email Error: " + err);
      }
    }
    
    // Update statuses
    // Assuming col lengths: 7 (fixed lead) + columns.length + 1 (privacy) + 2 (statuses)
    const statusStartCol = 7 + settings.columns.length + 1;
    sheet.getRange(newRowIndex, statusStartCol + 1).setValue(autoReplyStatus);
    sheet.getRange(newRowIndex, statusStartCol + 2).setValue(adminNotifyStatus);
    
    return ContentService.createTextOutput(JSON.stringify({"status": "success", "id": recordId}))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": err.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Simple English Key mapping to support English forms mapped to Japanese columns
function getEnglishKey(jpKey) {
  const map = {
    "氏名": "name", 
    "ふりがな": "kana",
    "メールアドレス": "email",
    "電話番号": "phone",
    "会社名・団体名": "company",
    "お問い合わせ種別": "inquiry_type",
    "お問い合わせ内容": "message",
    "年齢": "age",
    "希望職種": "job_type",
    "勤務希望条件": "conditions",
    "応募動機・自由記述": "motivation",
    "保有資格": "qualifications",
    "現在の勤務状況": "current_status",
    "見学希望の有無": "tour_request",
    "希望内容": "request_type",
    "希望日時": "preferred_datetime",
    "年齢層": "age_group",
    "健康上の配慮事項": "health_concerns",
    "備考": "memo",
    "ご本人との関係": "relationship",
    "主な相談内容": "main_concern",
    "お悩みの部位・箇所": "pain_area",
    "訪問希望地域": "visit_area",
    "介護認定の有無": "care_certification",
    "医師・ケアマネの関与有無": "medical_involvement",
    "希望連絡方法": "contact_method",
    "現在の困りごと": "current_trouble",
    "利用希望者の年齢層": "user_age_group",
    "ケアマネ有無": "has_care_manager",
    "相談種別": "consultation_type",
    "相談内容": "consultation_details",
    "面談希望方法": "meeting_method",
    "所属先": "affiliation",
    "問い合わせ種別": "partner_inquiry_type",
    "問い合わせ内容": "partner_inquiry_details"
  };
  return map[jpKey] || jpKey;
}
