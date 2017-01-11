## SearchConsoleApp 
- A cli/terminal based app for client, written in python that used Webmaster's Search Console API to simplify the entire data flow from Google servers to your local client machine.
- Features:
	- **Simple:** 100% Client based. Simply create a local server and start using. _(Provided: Console has verified properties and Search Console API enabled with Oauth key generated already in order to authenticate client machine)._
	- **Secure:** Connection request enabled by oauth2. Muliple requests possible upon one time authentication. 
    - **Useful:** Get more out of [Search Console](https://www.google.com/webmasters/tools/home?hl=en) than what the actual google web console provides. For instance: Google lets you download max. 1000 rows of data. SearchConsoleApp let's you download as much data as possible, with multiple secret arguments in combinations, typically not possible with the Web App. See [Google's api doc](https://developers.google.com/webmaster-tools/v3/how-tos/search_analytics) to find out more.
    - More: 
    	- Module based: Use it like one application or use a part of it.
        - Cleanses incoming data and saves then in usable .csv files. 
        - Files are in a ready to go for database format (mysql).
        - run directly from your terminal/cmd line

#### This App basically works as a Data pipeline to extract everything that the Google Webmaster as to offer.####
--
**Techstack and more about SearchConsoleApp**
- Search Console Api (Google Webmaster)
- python (core)
	- py modules: http, oauth2, sys, argv, pandas, os.
- shell
- db
	- local instance: MySQL
    - Integrated: Big Query
- ds: hash, arrays, hash in a array etc.

Dependencies before using the app:
- Google’s python-gflags
- [httplib2](https://github.com/jcgregorio/httplib2)
- [google-api-python-client](https://github.com/google/google-api-python-client)
- apache local host (for client machine, you can install xampp/mamp) : optional.

-- 