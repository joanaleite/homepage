// Light / dark mode switch, shared by every page.

// 1. Choose the starting theme: the visitor's last choice, otherwise the system setting
const saved = localStorage.getItem("theme");
const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
let theme = saved || (systemDark ? "dark" : "light");

// Apply it straight away to <html> (this script runs in <head>, before the page is drawn)
document.documentElement.dataset.theme = theme;

// 2. When the page is ready, make the button work
document.addEventListener("DOMContentLoaded", () => {
  const button = document.querySelector(".theme-toggle");
  button.setAttribute("aria-pressed", theme === "dark");

  button.addEventListener("click", () => {
    theme = theme === "dark" ? "light" : "dark";      // flip the theme
    document.documentElement.dataset.theme = theme;   // CSS reacts to data-theme
    button.setAttribute("aria-pressed", theme === "dark");
    localStorage.setItem("theme", theme);             // remember it on the next visit
  });
});
