// The following break classes are handled by the pair table
exports.OP = 0;   // Opening punctuation
exports.CL = 1;   // Closing punctuation
exports.CP = 2;   // Closing parenthesis
exports.QU = 3;   // Ambiguous quotation
exports.GL = 4;   // Glue
exports.NS = 5;   // Non-starters
exports.EX = 6;   // Exclamation/Interrogation
exports.SY = 7;   // Symbols allowing break after
exports.IS = 8;   // Infix separator
exports.PR = 9;   // Prefix
exports.PO = 10;  // Postfix
exports.NU = 11;  // Numeric
exports.AL = 12;  // Alphabetic
exports.HL = 13;  // Hebrew Letter
exports.ID = 14;  // Ideographic
exports.IN = 15;  // Inseparable characters
exports.HY = 16;  // Hyphen
exports.BA = 17;  // Break after
exports.BB = 18;  // Break before
exports.B2 = 19;  // Break on either side (but not pair)
exports.ZW = 20;  // Zero-width space
exports.CM = 21;  // Combining marks
exports.WJ = 22;  // Word joiner
exports.H2 = 23;  // Hangul LV
exports.H3 = 24;  // Hangul LVT
exports.JL = 25;  // Hangul L Jamo
exports.JV = 26;  // Hangul V Jamo
exports.JT = 27;  // Hangul T Jamo
exports.RI = 28;  // Regional Indicator
exports.EB = 29;  // Emoji Base
exports.EM = 30;  // Emoji Modifier
exports.ZWJ = 31; // Zero Width Joiner
exports.CB = 32;  // Contingent break

// The following break classes are not handled by the pair table
exports.AI = 33;  // Ambiguous (Alphabetic or Ideograph)
exports.BK = 34;  // Break (mandatory)
exports.CJ = 35;  // Conditional Japanese Starter
exports.CR = 36;  // Carriage return
exports.LF = 37;  // Line feed
exports.NL = 38;  // Next line
exports.SA = 39;  // South-East Asian
exports.SG = 40;  // Surrogates
exports.SP = 41;  // Space
exports.XX = 42;  // Unknown
