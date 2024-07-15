function createReport(data) {
  console.log("Creating report...");
  for (const url in data) {
    console.log(`Found ${data[url]} internal links to ${url}`);
  }
}

export { createReport };
