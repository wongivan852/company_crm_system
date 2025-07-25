# 🔐 UAT Access Guide - Secured Public Views

## Security Changes Made

The previously unsecured public views have been secured with token-based access control and configuration flags.

## Access URLs (Development)

**Base URL:** `http://localhost:8000/`

### Required Parameters
All UAT views now require an access token:
- **Token:** `secure-uat-token-dev-2024` (development)
- **Parameter:** `?token=secure-uat-token-dev-2024`

### Available UAT Endpoints

1. **Dashboard:**
   ```
   http://localhost:8000/?token=secure-uat-token-dev-2024
   ```

2. **Customer List:**
   ```
   http://localhost:8000/customers/?token=secure-uat-token-dev-2024
   ```

3. **Create Customer:**
   ```
   http://localhost:8000/customers/create/?token=secure-uat-token-dev-2024
   ```

## Secure Production Access

In production, UAT views should be disabled by setting:
```env
ENABLE_PUBLIC_UAT_VIEWS=False
```

## Alternative: Use Secure Login Views

For production use, access the secure views that require authentication:

1. **Secure Dashboard:** `/secure/`
2. **Secure Customer List:** `/secure/customers/`
3. **Secure Customer Create:** `/secure/customers/create/`

## API Rate Limiting

The following rate limits are now enforced:
- **Anonymous users:** 100 requests/hour
- **Authenticated users:** 1000 requests/hour
- **Login attempts:** 10 attempts/minute

## Security Features Added

✅ **Token-based access control** for UAT views
✅ **Configuration flag** to disable UAT views
✅ **Rate limiting** on API endpoints
✅ **Authentication required** for CSV export
✅ **Throttling** on sensitive operations

## For Developers

### Environment Configuration

**Development (.env):**
```env
ENABLE_PUBLIC_UAT_VIEWS=True
UAT_ACCESS_TOKEN=secure-uat-token-dev-2024
```

**Production (.env.production):**
```env
ENABLE_PUBLIC_UAT_VIEWS=False
UAT_ACCESS_TOKEN=disabled
```

### Testing Access

```bash
# Test protected endpoint without token (should fail)
curl http://localhost:8000/customers/

# Test with valid token (should work)
curl "http://localhost:8000/customers/?token=secure-uat-token-dev-2024"
```

## Important Notes

⚠️ **Never use UAT views in production**
⚠️ **Always use secure authentication for production**
⚠️ **Change the UAT token regularly**
⚠️ **Monitor access logs for unauthorized attempts**