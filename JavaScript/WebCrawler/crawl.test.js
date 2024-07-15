import { test, expect } from "@jest/globals";
import { normaliseURL } from "./crawl.js";

test("Returns the normalised URL", () => {
  const input = "https://www.arbabansari.com/home";
  const expected = "www.arbabansari.com/home";
  const actual = normaliseURL(input);

  expect(actual).toBe(expected);
});

test("Returns the normalised URL", () => {
  const input = "https://www.arbabansari.com/home/";
  const expected = "www.arbabansari.com/home";
  const actual = normaliseURL(input);

  expect(actual).toBe(expected);
});

test("Returns the normalised URL", () => {
  const input = "http://www.arbabansari.com/home/";
  const expected = "www.arbabansari.com/home";
  const actual = normaliseURL(input);

  expect(actual).toBe(expected);
});

test("Returns the normalised URL", () => {
  const input = "https://www.arbabansari.com:80/home/";
  const expected = "www.arbabansari.com/home";
  const actual = normaliseURL(input);

  expect(actual).toBe(expected);
});

test("Returns array of anchor elements", () => {
  const input = undefined;
});
