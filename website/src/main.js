import "@fontsource-variable/dm-sans";
import "@fontsource/instrument-serif/latin-400-italic.css";
import "./style.css";

const iconPaths = {
  search:
    '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5M7 10.5h7M10.5 7v7"/>',
  boxes:
    '<path d="m12 3 8 4.5v9L12 21l-8-4.5v-9L12 3Zm-8 4.5 8 4.5 8-4.5M12 12v9M8 5.25l8 4.5"/>',
  arrow: '<path d="M3 8h12M3 12h8M3 16h5M14 6l7 6-7 6M11 12h10"/>',
  shield:
    '<path d="m12 3 8 3v6c0 4-4 7-8 9-4-2-8-5-8-9V6l8-3Z"/><path d="m8 12 3 3 5-6"/>',
  sliders:
    '<path d="M4 6h16M4 12h16M4 18h16"/><circle cx="9" cy="6" r="2"/><circle cx="16" cy="12" r="2"/><circle cx="8" cy="18" r="2"/>',
  globe:
    '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M5 6.5h14M5 17.5h14"/>',
};
document.querySelectorAll("[data-icon]").forEach((element) => {
  element.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${iconPaths[element.dataset.icon]}</svg>`;
});
const arrowPaths = {
  "↗": "M5 19 19 5M5 5h14v14",
  "↘": "M5 5 19 19M5 19h14V5",
  "↑": "M12 21V3M5 10l7-7 7 7",
};
document.querySelectorAll('span[aria-hidden="true"]').forEach((element) => {
  const path = arrowPaths[element.textContent.trim()];
  if (path) {
    element.classList.add("direction-icon");
    element.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="${path}"/></svg>`;
  }
});
document.querySelector("#year").textContent = new Date().getFullYear();

const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#main-navigation");
function closeMenu() {
  menuButton.setAttribute("aria-expanded", "false");
  menuButton.setAttribute("aria-label", "Open navigation");
  navigation.classList.remove("is-open");
}
menuButton.addEventListener("click", () => {
  const open = menuButton.getAttribute("aria-expanded") !== "true";
  menuButton.setAttribute("aria-expanded", String(open));
  menuButton.setAttribute(
    "aria-label",
    open ? "Close navigation" : "Open navigation",
  );
  navigation.classList.toggle("is-open", open);
});
navigation
  .querySelectorAll("a")
  .forEach((link) => link.addEventListener("click", closeMenu));
document.addEventListener("keydown", (event) => {
  if (
    event.key === "Escape" &&
    menuButton.getAttribute("aria-expanded") === "true"
  ) {
    closeMenu();
    menuButton.focus();
  }
});
window.matchMedia("(min-width: 901px)").addEventListener("change", (event) => {
  if (event.matches) closeMenu();
});

const dialog = document.querySelector("#quote-dialog");
const form = document.querySelector("#quote-form");
const review = document.querySelector("#quote-review");
const partInput = form.elements.part;
let dialogTrigger;
function openQuote(part = "", trigger = document.activeElement) {
  closeMenu();
  dialogTrigger = trigger;
  form.hidden = false;
  review.hidden = true;
  document.querySelector("#copy-status").textContent = "";
  if (part) partInput.value = part;
  dialog.showModal();
  document.body.classList.add("dialog-open");
  form.elements.name.focus();
}
document.querySelectorAll("[data-quote]").forEach((button) => {
  button.addEventListener("click", () =>
    openQuote(button.dataset.quote, button),
  );
});
document.querySelector("#part-search").addEventListener("submit", (event) => {
  event.preventDefault();
  const query = document.querySelector("#part-query").value.trim();
  if (query) openQuote(query, document.querySelector("#part-search button"));
});
document
  .querySelector(".dialog-close")
  .addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (event) => {
  if (event.target === dialog) {
    const rect = dialog.getBoundingClientRect();
    if (
      event.clientX < rect.left ||
      event.clientX > rect.right ||
      event.clientY < rect.top ||
      event.clientY > rect.bottom
    )
      dialog.close();
  }
});
dialog.addEventListener("close", () => {
  document.body.classList.remove("dialog-open");
  dialogTrigger?.focus();
});
form.addEventListener("submit", (event) => {
  event.preventDefault();
  const values = Object.fromEntries(new FormData(form));
  const fields = ["name", "company", "email", "part"];
  for (const field of fields) {
    if (!values[field].trim()) {
      form.elements[field].setCustomValidity("Please enter this information.");
      form.elements[field].reportValidity();
      return;
    }
  }
  const subject = `Parts inquiry — ${values.company.trim()} — ${values.part.trim()}`;
  const body = `Hello Saif Industries team,\n\nI'd like to request availability and a quote for:\n\nPart / description: ${values.part.trim()}\nQuantity: ${values.quantity}\nRequired condition: ${values.condition}\n\nDelivery, documentation & other requirements:\n${values.notes.trim() || "Please discuss with me."}\n\nContact name: ${values.name.trim()}\nCompany: ${values.company.trim()}\nEmail: ${values.email.trim()}\n\nPlease confirm availability and next steps. Thank you.`;
  document.querySelector("#email-inquiry").href =
    `mailto:sales@saifind.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  document.querySelector("#inquiry-preview").value = `${subject}\n\n${body}`;
  form.hidden = true;
  review.hidden = false;
  document.querySelector("#email-inquiry").focus();
});
form.addEventListener("input", (event) => {
  if (event.target.setCustomValidity) event.target.setCustomValidity("");
});
document.querySelector("#edit-inquiry").addEventListener("click", () => {
  review.hidden = true;
  form.hidden = false;
  partInput.focus();
});
document.querySelector("#copy-inquiry").addEventListener("click", async () => {
  const preview = document.querySelector("#inquiry-preview");
  const status = document.querySelector("#copy-status");
  try {
    await navigator.clipboard.writeText(preview.value);
    status.textContent = "Copied. Paste into an email to sales@saifind.com.";
  } catch {
    preview.focus();
    preview.select();
    status.textContent =
      "Select and copy the highlighted inquiry, then email sales@saifind.com.";
  }
});
