# Learning Institute CRM - Security Update

## 🔒 UAT Views Disabled - Secure Login Required

**Effective immediately, all CRM functions require secure authentication.**

### What Changed:
- ❌ Public UAT access has been **disabled for security**
- ✅ All customer data operations now require **authenticated login**
- 🔐 Secure authentication protects sensitive customer information
- 🛡️ Enhanced security measures are now in place

### How to Access:
1. Navigate to: `http://127.0.0.1:8000/`
2. You will be automatically redirected to the secure login page
3. Login with your credentials:
   - **Username**: `adminadmin`
   - **Password**: [Use the password you set during creation]

### Available Features (After Login):
- ✅ Customer Dashboard
- ✅ Customer List & Search
- ✅ Add/Edit Customer Information
- ✅ Export Customer Data (CSV)
- ✅ International Phone Number Support
- ✅ All Enhanced Customer Data Fields

### Security Features:
- 🔐 Session-based authentication
- 🕐 Auto-logout after 1 hour of inactivity
- 🛡️ CSRF protection
- 🚫 UAT token access disabled
- 💾 Secure session management

### For Administrators:
- Update environment variables: `ENABLE_PUBLIC_UAT_VIEWS=False`
- All previous UAT endpoints now redirect to secure login
- User management available through Django admin panel

**Security is our priority. Contact your system administrator if you need access credentials.**
