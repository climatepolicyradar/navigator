import Document, { Html, Head, Main, NextScript } from "next/document";
import getSite from "@utils/getSite";

class MyDocument extends Document {
  site = getSite();
  favicon = this.site === "cclw" ? "/cclw/images/favicon.png" : "/favicon.png";

  render() {
    return (
      <Html lang="en" id={this.site}>
        <Head>
          <link rel="icon" href={this.favicon} />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}

export default MyDocument;
