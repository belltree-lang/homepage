/**
 * Google Apps Script Web App for BellTree Forms
 * Handles 7 different form types, writes to appropriate sheets, and sends auto-replies.
 * 
 * Target Spreadsheet ID: 1fZn6nxbQ_kFXZXwxKNr97R_QxzcVM5HXlfLyiBOuJes
 */

const CONFIG = {
  SPREADSHEET_ID: "1fZn6nxbQ_kFXZXwxKNr97R_QxzcVM5HXlfLyiBOuJes",
  ADMIN_EMAIL: "belltree@belltree1102.com",
  COMPANY_NAME: "株式会社べるつりー",
  COMPANY_PHONE: "042-682-2839",
  COMPANY_ADDRESS: "東京都八王子市下柚木3-7-2-401"
};

// Form mappings to their specific settings
// Columns must match the 'name' attributes in the HTML forms or be mapped via getEnglishKey
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
    columns: ["ご本人との関係", "氏名", "メールアドレス", "電話番号", "主な相談内容", "お悩みの部位・箇所", "訪問希望地域", "介護認定の有無", "医師・ケアマネの関与有無", "希望連絡方法", "備考"]
  },
  "daycare_consultations": {
    sheetName: "daycare_consultations",
    prefix: "DAY",
    subject: "【べるフィット】通所リハ・介護相談を受け付けました",
    senderName: "べるフィット",
    columns: ["ご本人との関係", "氏名", "メールアドレス", "電話番号", "現在の困りごと", "利用希望者の年齢層", "要支援・要介護認定の有無", "ケアマネ有無", "見学希望日時", "備考"]
  },
  "legal_consultations": {
    sheetName: "legal_consultations",
    prefix: "LEG",
    subject: "【べるリーガル行政書士事務所】ご相談を受け付けました",
    senderName: "べるリーガル行政書士事務所",
    columns: ["氏名", "メールアドレス", "電話番号", "相談種別", "面談希望方法", "相談内容", "年齢層", "希望日時", "備考"]
  },
  "partner_inquiries": {
    sheetName: "partner_inquiries",
    prefix: "PAR",
    subject: "【株式会社べるつりー 地域連携窓口】お問い合わせを受け付けました",
    senderName: "株式会社べるつりー 地域連携窓口",
    columns: ["担当者名", "法人名_屋号", "部署_役職", "メールアドレス", "電話番号", "問い合わせ種別", "問い合わせ内容", "URL", "備考"]
  }
};

/**
 * Handles GET requests (for testing and verification)
 */
function doGet(e) {
  try {
    const activeSpreadsheet = SpreadsheetApp.openById(CONFIG.SPREADSHEET_ID);
    return ContentService.createTextOutput(JSON.stringify({
      status: "ok",
      service: "BellTree Form Service",
      spreadsheetId: CONFIG.SPREADSHEET_ID,
      spreadsheetName: activeSpreadsheet.getName(),
      timestamp: new Date().toISOString()
    })).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Handles POST requests from the website forms
 */
function doPost(e) {
  console.log("doPost triggered");
  if (!e || !e.postData || !e.postData.contents) {
    console.error("Empty request data");
    return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "No data received"}))
      .setMimeType(ContentService.MimeType.JSON);
  }

  try {
    const data = JSON.parse(e.postData.contents);
    console.log("Parsed data: " + JSON.stringify(data));
    
    const formType = data.formType;
    if (!FORM_MAP[formType]) {
      throw new Error("Invalid formType: " + formType);
    }
    
    const settings = FORM_MAP[formType];
    const timestamp = new Date();
    
    // Process Spreadsheet Writing
    console.log("Opening spreadsheet: " + CONFIG.SPREADSHEET_ID);
    const ss = SpreadsheetApp.openById(CONFIG.SPREADSHEET_ID);
    const sheet = ss.getSheetByName(settings.sheetName);
    
    if (!sheet) {
      console.error("Sheet not found: " + settings.sheetName);
      throw new Error("Sheet not found: " + settings.sheetName);
    }
    
    // Generate ID
    const dateStr = Utilities.formatDate(timestamp, "JST", "yyyyMMdd");
    const lastRow = Math.max(sheet.getLastRow(), 1);
    const sequenceObj = Utilities.formatString("%04d", lastRow); 
    const recordId = `${settings.prefix}-${dateStr}-${sequenceObj}`;
    
    // Prepare standard Lead columns (1-7)
    let rowData = [
      timestamp, 
      formType, 
      recordId, 
      "未対応", 
      "", // Assigned
      "", // Notes
      ""  // Source
    ];
    
    // Form Specific Columns
    settings.columns.forEach(col => {
      const val = data[col] || data[getEnglishKey(col)] || "";
      rowData.push(val);
    });
    
    const privacyAgreement = data.privacy_agreement ? "同意済" : "未同意";
    rowData.push(privacyAgreement);
    rowData.push("未送信"); // Auto-reply status placeholder
    rowData.push("未送信"); // Admin notify status placeholder
    
    // Append to sheet
    console.log("Appending row to sheet: " + settings.sheetName);
    sheet.appendRow(rowData);
    const newRowIndex = sheet.getLastRow();
    
    // Send Emails
    let autoReplyStatus = "失敗";
    let adminNotifyStatus = "失敗";
    
    // Detect email and name for auto-reply
    const userEmail = data.email || data["メールアドレス"] || data["メールアドレス_必須"];
    const userName = data.name || data["氏名"] || data["担当者名"] || "お客様";
    
    // 1. Admin Notification
    try {
      console.log("Sending admin email to: " + CONFIG.ADMIN_EMAIL);
      const adminBody = `Webサイトから新しいフォーム送信がありました。\n\n`
        + `◆受付番号: ${recordId}\n`
        + `◆フォーム種別: ${formType}\n`
        + `◆お名前: ${userName}\n\n`
        + `確認はスプレッドシート（${settings.sheetName}シート）より行ってください。\n`;
      
      MailApp.sendEmail({
        to: CONFIG.ADMIN_EMAIL,
        subject: `【Web通知】${recordId} 新規お問い合わせ（${userName}様）`,
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
        console.log("Sending auto-reply to: " + userEmail);
        let extraText = "内容を確認のうえ、通常2営業日以内を目安にご連絡いたします。\n";
        if (formType === "recruit_applications") {
          extraText = "書類提出や見学調整が必要な場合は、改めてご案内いたします。\n";
        } else if (formType === "partner_inquiries") {
          extraText = "地域連携担当より、内容を確認のうえご連絡いたします。\n";
        }
        
        const autoReplyBody = `${userName} 様\n\n`
          + `この度はお問い合わせいただき、誠にありがとうございます。\n`
          + `送信が完了いたしました。\n\n`
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
    
    // Update statuses in the sheet
    // Status columns are at the end: Privacy, Auto-reply, Admin Notify
    const statusStartCol = 7 + settings.columns.length + 1;
    sheet.getRange(newRowIndex, statusStartCol + 1).setValue(autoReplyStatus);
    sheet.getRange(newRowIndex, statusStartCol + 2).setValue(adminNotifyStatus);
    
    console.log("Successfully processed: " + recordId);
    return ContentService.createTextOutput(JSON.stringify({"status": "success", "id": recordId}))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (err) {
    console.error("Fatal Error in doPost: " + err);
    return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": err.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Simple English Key mapping to support English forms mapped to Japanese columns
function getEnglishKey(jpKey) {
  const map = {
    "氏名": "name", 
    "担当者名": "name",
    "ふりがな": "kana",
    "メールアドレス": "email",
    "電話番号": "phone",
    "会社名・団体名": "company",
    "法人名_屋号": "affiliation",
    "部署_役職": "dept",
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
ewRowIndex, statusStartCol + 2).setValue(adminNotifyStatus);
    
    console.log("Successfully processed: " + recordId);
    return ContentService.createTextOutput(JSON.stringify({"status": "success", "id": recordId}))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (err) {
    console.error("Fatal Error in doPost: " + err);
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
