# How the visualization was created in Tableau and how to use it

## Dashboard 1: Top 5 NFTs in each Dapp
This dashboard shows the number of NFTs and the images of top 5 NFTs in each Dapp
### Creation steps:
1. In a new worksheet, create a table of Dapp name and its number of NFTs. Put the IDs of top 5 NFTs in the Tooltip, and the image URLs of those NFTs in the Details.
2. Choose Dapp name as the field for filtering, make it appear as Single Value Dropdown.
3. Create a new dashboard and drag this worksheet in. Drag to the dashboard 5 Extension objects where the images of top 5 NFTs are planned to be located.
4. Choose Image Viewer Extension to be the type of Tableau Extension for the 5 objects. Choose to show the image at "Filter Changed", and put in the field in the dataset that contains the URL needed for showing each of the 5 images.
5. Put a text box object above each of the 5 images to label the images from top 1 to 5, to indicate the ranking of each NFT

### How to use the plot:
1. When a Dapp is picked from the dropdown button, the plot shows the images of top 5 NFTs in the Dapp, along with a table with the Dapp's name and number of NFTs within it
2. Hover to the number of NFTs of the Dapp in the table, a tooltip will appear and show the IDs of the top 5 NFTs

## Dashboard 2: Original & Predicted Price w.r.t. Rarity
For each Dapp, this dashboard shows the relationship between an NFT's rarity, real price, and predicted price based on rarity using Linear Regression.
### Creation steps:
1. In a new worksheet, create a scatter plot of Rarity (x) against Last Sale Total Price (y) in Etherium (ETH). Make sure to change the two fields' type to Dimension instead of Measure. Reduce the opacity of the points to 30% make them look clearer
2. Drag the Predicted Price field to the right side of the scatter plot to make a second vertical axis for the graph, and synchronize this axis with the previous vertical axis. Set Predicted Price to appear as a line. Increase the opacity of the line to 60% to make it look clearer.
3. Drag the NFT name to the Tooltip
4. Choose Dapp name as the field for filtering, make it appear as Single Value Dropdown
5. Drag this worksheet to a new dashboard
### How to use the plot:
1. Pick a dapp from the dropdown button, the graph will show the rarity, original price, and predicted price of all NFTs in this dapp. The original price appears as scatters, and the predicted price appears as a line.
2. Hover to any scatters or points in the line to see the name of the NFT and its actual/predicted price in ETH

## Dashboard 3: Daily, Weekly, and Monthly Volume Trends for the Top 10 Dapps with the Highest Market Capacity
This dashboard shows the daily, weekly, and monthly volume of top 10 Dapps with the highest market capacity
### Creation steps:
1. Open 3 new worksheets, in each of which create a bar chart that shows the 1-day, 7-day, and 30 day volume of the 10 Dapps
2. Create a new user-defined parameter “Trend Selection”, with values “1-day trend”, “7-day trend”, and “30-day trend”, corresponding to the 3 graphs
3. Create a new Calculated Field (user-defined field) “Selected Trend” with values based on the Trend Selection parameter.
4. Choose this Selected Trend field for filtering. Make the 1-day trend graph appear only when the "1-day Trend" box is checked. The same step applies to the 7-day and 30-day graphs.
5. Create a new dashboard and drag in a container to define the area used for the 3 charts. Choose the “Titled” option when dragging the charts to the container so that the charts take up the whole space in the container. This ensures that every graph appears with the same size and in the same space when it is chosen to be displayed.
6. Choose to show the Selected Trend parameter as a dropdown button


### How to use the plot:
From the dropdown button, choose 1-day trend, 7-day trend, or 30-day trend, the corresponding graph will appear.

## Dashboard 4: Optimal & Suboptimal Collections
This dashboard shows the number of optimal and suboptimal collections among the 100 collections, and the names of the collections in each category.
### Creation steps:
1. In a new worksheet, drag Optimal.json(Count) to Size, and Ratio to Color and Label. If the visualization does not automatically show up as a bubble chart, click on Show Me and choose bubble chart as the type of graph for this case
2. In another worksheet, create a table of Dapp name and Ratio. This table shows which Dapps are optimal and suboptimal
3. Create a new dashboard and drag the two worksheets in. Turn on the Filter button next to the bubble chart

### How to use the plot:
1. Hover to a bubble to see the number of collections belong to this category (Optimal or Suboptimal)
2. When the Optimal bubble is clicked, the table will show all the optimal collections. When the Suboptimal bubble is clicked, the table will show all the suboptimal collections.

## Dashboard 5: Price vs Number of Sales Correlation for each Dapp
This dashboard shows the Pearson Correlation between the Price and Number of Sales for different Dapps.
### Creation steps:
1. In a new worksheet, create a bar chart to illustrate the Price vs Number of Sales Correlation for all the Dapps.
2. Create a new dashboard and drag this worksheet in. Choose "Fit -> Entire View" in order to see the whole chart without scrolling. Adjust the size of the chart so that all the Dapp names are shown clearly since the number of Dapps is quite large.


### How to use the plot:
The plot gives a clear idea of whether the correlation between price and sales is positive and negative for each Dapp. To see the exact correlation number for a Dapp, hover to its corresponding bar.
