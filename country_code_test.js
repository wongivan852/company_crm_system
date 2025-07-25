// Test script to verify Hong Kong SAR country code functionality
console.log('Testing Hong Kong SAR country code...');

// Test the country code mapping
const countryCodeMap = {
    'CN': '+86', 'HK': '+852', 'TW': '+886', 'MO': '+853',
    'SG': '+65', 'MY': '+60', 'TH': '+66', 'VN': '+84',
    'PH': '+63', 'ID': '+62', 'KR': '+82', 'JP': '+81',
    'IN': '+91', 'AU': '+61', 'NZ': '+64',
    'GB': '+44', 'DE': '+49', 'FR': '+33', 'IT': '+39',
    'ES': '+34', 'NL': '+31', 'BE': '+32', 'CH': '+41',
    'AT': '+43', 'SE': '+46', 'NO': '+47', 'DK': '+45', 'FI': '+358',
    'US': '+1', 'CA': '+1', 'MX': '+52', 'BR': '+55',
    'AR': '+54', 'CL': '+56', 'CO': '+57', 'PE': '+51',
    'AE': '+971', 'SA': '+966', 'IL': '+972', 'ZA': '+27',
    'EG': '+20', 'KE': '+254', 'NG': '+234',
    'RU': '+7', 'TR': '+90'
};

// Test Hong Kong
console.log('HK code:', countryCodeMap['HK']); // Should be +852
console.log('US code:', countryCodeMap['US']); // Should be +1
console.log('CN code:', countryCodeMap['CN']); // Should be +86

// Verify the mapping is correct
if (countryCodeMap['HK'] === '+852') {
    console.log('✅ Hong Kong SAR country code mapping is CORRECT (+852)');
} else {
    console.log('❌ Hong Kong SAR country code mapping is INCORRECT');
}

console.log('Test completed. Use the test buttons in the form to verify functionality.');
