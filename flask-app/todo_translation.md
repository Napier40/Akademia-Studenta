# Automated Translation Implementation Plan

## Current State Analysis
- [x] Flask-Babel already installed and configured
- [x] Language switcher exists in navigation (EN/PL)
- [x] Manual translations exist in translations/pl/LC_MESSAGES/messages.po
- [x] Session-based language switching implemented
- [x] Database has bilingual fields (title_en, title_pl, content_en, content_pl)

## Goal
Implement automated translation with minimal manual intervention for:
1. UI text (buttons, labels, messages)
2. Blog post content (customer submissions in single language)
3. Dynamic content (comments, inquiries)

## Implementation Strategy

### Phase 1: Automated UI Translation
- [ ] Integrate Google Translate API or DeepL API
- [ ] Create translation service module
- [ ] Auto-translate missing UI strings
- [ ] Update .po files automatically

### Phase 2: Content Translation
- [ ] Auto-translate blog posts when published
- [ ] Translate customer submissions to missing language
- [ ] Cache translations in database
- [ ] Add translation quality indicator

### Phase 3: Enhanced User Experience
- [ ] Add visual toggle switch in menu bar
- [ ] Show loading indicator during translation
- [ ] Add "Original language" badge
- [ ] Implement translation fallback

### Phase 4: Performance Optimization
- [ ] Cache translations in Redis/memory
- [ ] Batch translation requests
- [ ] Lazy load translations
- [ ] CDN for static translations

## Recommended Approach
1. Use DeepL API (better quality for EN-PL)
2. Translate on-demand with caching
3. Store translations in database
4. Manual review option for important content