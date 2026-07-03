![[clash.png]]
```.layout,
.base-page,
.MuiPaper-root,
.MuiDialog-paper,
.MuiMenu-paper,
.MuiPopover-paper,
.MuiDrawer-paper {
  background:
    radial-gradient(circle at top left, rgba(255, 214, 224, 0.54), transparent 30%),
    linear-gradient(180deg, #fffaf8 0%, #fff4f3 55%, #fcecef 100%) !important;
  color: #4f3b43 !important;
}

.layout::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  opacity: 0.1;
  background:
    repeating-linear-gradient(0deg,
      rgba(160, 102, 121, 0.05) 0,
      rgba(160, 102, 121, 0.05) 1px,
      transparent 1px,
      transparent 6px);
}

.layout-content__left {
  background: linear-gradient(180deg, rgba(255, 249, 247, 0.96), rgba(250, 236, 240, 0.94)) !important;
  border-right: 1px solid rgba(233, 154, 174, 0.26) !important;
}

.the-logo,
.the_titlebar,
.base-page>header,
.MuiDialogTitle-root {
  background: rgba(255, 252, 251, 0.62) !important;
  backdrop-filter: blur(12px) saturate(125%) !important;
  border-bottom: 1px solid rgba(233, 154, 174, 0.2) !important;
}

.the-menu .MuiListItemButton-root {
  margin: 6px 10px !important;
  border-radius: 14px !important;
  color: #7f5565 !important;
  transition: background 0.2s ease, color 0.2s ease !important;
}

.the-menu .MuiListItemButton-root:hover {
  background: rgba(255, 215, 225, 0.4) !important;
  color: #b35e79 !important;
}

.the-menu .MuiListItemButton-root.Mui-selected,
.the-menu .MuiListItemButton-root[aria-current="page"] {
  background: linear-gradient(135deg, #f6c2cf, #e99aae) !important;
  color: #fffaf7 !important;
}

.the-menu .MuiListItemButton-root.Mui-selected .MuiListItemIcon-root,
.the-menu .MuiListItemButton-root.Mui-selected .MuiTypography-root {
  color: #fffaf7 !important;
}

.MuiPaper-root,
.MuiCard-root,
.MuiDialog-paper,
.MuiMenu-paper,
.MuiPopover-paper {
  border-radius: 18px !important;
  background: rgba(255, 252, 250, 0.78) !important;
  border: 1px solid rgba(233, 154, 174, 0.2) !important;
  box-shadow:
    0 12px 28px rgba(184, 133, 149, 0.12),
    0 2px 10px rgba(233, 154, 174, 0.08) !important;
  backdrop-filter: blur(14px) saturate(120%) !important;
}

.MuiButton-root,
.MuiChip-root,
.MuiOutlinedInput-root,
.MuiAccordionSummary-root,
.MuiTab-root {
  border-radius: 14px !important;
}

.MuiButton-containedPrimary,
.MuiButton-contained.MuiButton-colorPrimary {
  background: linear-gradient(135deg, #e99aae, #ffb7c5) !important;
  color: #fffdfb !important;
}

.MuiButton-outlined,
.MuiButton-text {
  color: #bb6a85 !important;
  border-color: rgba(233, 154, 174, 0.28) !important;
  background: rgba(255, 255, 255, 0.34) !important;
}

.MuiOutlinedInput-root {
  background: rgba(255, 255, 255, 0.68) !important;
}

.MuiOutlinedInput-root fieldset {
  border-color: rgba(233, 154, 174, 0.3) !important;
}

.MuiOutlinedInput-root:hover fieldset {
  border-color: rgba(217, 107, 136, 0.56) !important;
}

.MuiOutlinedInput-root.Mui-focused fieldset {
  border-color: #e99aae !important;
  box-shadow: 0 0 0 3px rgba(233, 154, 174, 0.14) !important;
}

.MuiSwitch-switchBase.Mui-checked,
.MuiCheckbox-root.Mui-checked,
.MuiRadio-root.Mui-checked,
.MuiCheckbox-indeterminate,
.MuiInputLabel-root.Mui-focused,
.MuiFormLabel-root.Mui-focused,
.MuiTab-root.Mui-selected,
.MuiSlider-colorPrimary,
.MuiLink-root,
a {
  color: #c46f8b !important;
}

.MuiSwitch-switchBase.Mui-checked+.MuiSwitch-track {
  background-color: rgba(196, 111, 139, 0.46) !important;
}

.MuiLinearProgress-bar,
.MuiSlider-thumb,
.MuiSlider-track,
.MuiTabs-indicator {
  background: linear-gradient(135deg, #e99aae, #ffb7c5) !important;
  border-color: #e99aae !important;
}

.MuiChip-root {
  color: #8d5e6f !important;
  background: rgba(247, 223, 229, 0.82) !important;
  border: 1px solid rgba(233, 154, 174, 0.18) !important;
}

.MuiTypography-root,
.MuiButton-root,
.MuiInputBase-root,
.MuiListItemText-primary,
.MuiListItemText-secondary {
  letter-spacing: 0.015em !important;
}
```
