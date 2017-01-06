## google search console command line app ##

**Data pipeline to pull everything from that the google webmaster as to offer**
### Uses search analytics api
- Data is fetch from the api. Next, incoming data is cleansed, treated using pandas and np. 
- Works as a data pipeline. One app to download everything in a ready to go file format: csv.
- Looks for the system location, finds if the data request is already available on the local machine
- If not, creates the fodlers appropriately with sub fodlers
- Downloads everything and stores them into their appropriate folders automatically.
- In order to best utilize all the possible dimensions and filters that SA has to offer: 
- Data is pulled one by one from each of the scripts.
- Hack: User can fetch more than the max total rows permitted for downloads by the search console web, using this app.

-- 
*Complete infrastructure is built by me for using google cloud api services modules* 
