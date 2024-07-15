import { crawlPage } from "./crawl.js";
import { argv } from "node:process";
import { createReport } from "./report.js";

async function main() {
  console.log("Processing...");
  if (argv.length < 3) {
    throw new Error("No arguments were given need one");
  } else if (argv.length > 3) {
    throw new Error("More than one arguments were given need one");
  } else {
    console.log(`Crawling ${argv[2]}...`);
    const data = await crawlPage(argv[2]);
    createReport(data);
  }
}

await main();
