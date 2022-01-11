# Lightweight Destiny Weapon Analytics

## What is it?

LDWA is essentially an Android application that functions as a database browser, with the database being all the legendary, non-sunset weapons present in [Destiny 2](https://www.bungie.net/7/en/Destiny/NewLight), 
 made by Bungie, Inc. Currently, the app can browse the weapons present as of July, 2021. 
 
 On the main page, a variety of information is shown for each weapon, including the name, icon, element, and ammo type. 
 
 ![Main Page](/screenshots/main_ss.png)
 
 Clicking on a weapon opens up a view with a bit more information, including the weapon type, archetype, a screenshot, all the perks that can roll on this weapon,
 as well as a programmatically generated list of perks with good synergy. I categorized all perks based on trigger and effect, 
 and used some logic to highlight a roll if one perk from one category can roll with one perk from another particularly synergistic category. 
 This currently is quite primitive and refinement of those categories and whats listed as synergistic is planned for a future release. 
 
  ![Fragment View](/screenshots/fragment_ss.png)
 
 You can also save rolls of the weapon to the app, if you so please, and can go view those at any time, if perhaps you want to save a list of rolls you are seeking.
 
  ![Saved Rolls](/screenshots/saved_rolls_ss.png)
 
 ## How is it 'Lightweight'?
 
 The database is generated in Python, by myself, and that database is then passed to the LDWA application. 
 This database is only generated whenver Bungie's API is updated, so only once every couple weeks. 
 
 Since the database is stored locally on each device, that means to find the data, all that has to be done is a simple sql query, on a database that is only a few megabytes. 
 This is very quick and easy to do. 
 The images the app uses are all stored locally too, with the database only containing the filepaths of those images, so accessing those is very quick as well.
 
 This stands in contrast to the current solutions available. All the ones I know of are web-based, and make API calls to generate all the data they show you. For the most part this is fine, but it is a little slow, and requires you to have a good internet connection as well as making you load a new webpage everytime you want to view a new weapon. 
 LDWA uses DialogFragments (essentially, pop up windows in android apps) to show the full view of a weapon, which makes it very easy to click away or press the back button to close the fragment clickly and view another weapon, without changing the place you were looking in the main list. 
 
 ## Isn't [D2Gunsmith](https://D2Gunsmith.com) a far superior product?
 
Absolutely. There are some minor areas in which make this app have a niche that D2Gunsmith doesnt fill but by and large, D2Gunsmith is a much more fully featured product. I didnt make this app to be the best weapon viewer for destiny however, and I do not believe this really competes with D2Gunsmith at all.
 
 ## Why did you make it?
 
 Two main reasons: I wanted to view weapons very quickly and easily on my android phone, and I happened to be taking a course at my university which required me to build an android application. It seemed like the perfect time to address the first reason with a two birds, one stone approach. 
 
 It also gave me the oppurtunity to learn more about APIs, android programming in Java, Kotlin, as well as android UI development in XML, in addition to the work I did with python and SQL to generate the database. 
 
 ## How is the database generated?
 
 I generate the database using the code in the [python folder](/python). I retrieve the manifest from Bungie, which is a large compressed sql database with some 40+ tables, and thousands and thousands of rows in some of the tables, with each table having only one column, as each row is just one very large JSON string. I extract all the information I need through use of pandas' [DataFrames](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html) and [Series](https://pandas.pydata.org/pandas-docs/stable/reference/series.html). I then generate the much smaller sql database I need, and I retrieve the images with HTTP requests for the Bungie.net paths stored in my small database. These images and the database are then copied (later, this would be changed to something a little less... manual) to the android application, which will handle the rest. 
 
 ## How does the app work?
 
 A recyclerView and some SQL queries are used to display the database, as shown in the first screenshot above, with the full data in each row being displayed in the DialogFragment for each weapon. Data on the rolls you want saved is saved to the sql database, in a seperate table. This obviously would not persist if I copy and replace the database, which is why the datbase updating will be changed later to ensure that data persists. 
 
 ## How can I use the app? 

Go to the [releases page](https://github.com/Savathun/LDWA/releases) and download the APK from the latest release on to your android phone. Make sure you have the setting "Install from Unknown Sources" enabled on your phone. Then just click the file in your file manager, and android should do the rest. 
 
