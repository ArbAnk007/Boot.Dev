import { URL } from "node:url";
import { JSDOM } from "jsdom";

function normaliseURL(str) {
  const urlObj = new URL(str);
  const hostname = urlObj.hostname;
  const path =
    urlObj.pathname.slice(-1) === "/"
      ? urlObj.pathname.slice(0, -1)
      : urlObj.pathname;
  return `${hostname}${path}`;
}

function getURLsFromHTML(htmlBody, baseURL) {
  const { window } = new JSDOM(htmlBody);
  const { document } = window;
  const urlArr = [];
  const data = document.querySelectorAll("a");
  for (let url of data) {
    urlArr.push(url.getAttribute("href"));
  }
  const finalArr = urlArr.map((url) => {
    if (url[0] == "/") {
      return baseURL + url;
    }
    return url;
  });
  return finalArr;
}

async function getPageContent(url) {
  try {
    const response = await fetch(url);
    const data = await response.text();
    return data;
  } catch (error) {
    console.log(error);
  }
}

async function crawlPage(baseURL, currentURL = baseURL, pages = {}) {
  const baseURLObj = new URL(baseURL);
  const currentURLObj = new URL(currentURL);
  if (baseURLObj.hostname == currentURLObj.hostname) {
    const normalisedCurrentURL = normaliseURL(currentURL);
    if (normalisedCurrentURL in pages) {
      pages[normalisedCurrentURL] = pages[normalisedCurrentURL] + 1;
      return pages;
    } else {
      pages[normalisedCurrentURL] = 1;
    }

    const htmlBody = await getPageContent(currentURL);
    const urlArr = getURLsFromHTML(htmlBody, baseURL);
    if (urlArr.length) {
      for (let url of urlArr) {
        pages = await crawlPage(baseURL, url, pages);
      }
    } else {
      return pages;
    }
  }
  return pages;
}

export { normaliseURL, getURLsFromHTML, crawlPage };
