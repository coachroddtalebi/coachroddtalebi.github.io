<!--template from: https://v4-alpha.getbootstrap.com/getting-started/introduction/-->
<!--HOW TO USE PHP AND HTML: http://www.apaddedcell.com/how-automatically-include-your-header-navigation-and-footer-every-page -->

<!--include inside <head>-->
<title><?php echo $page_title; ?></title>
<meta http-equiv="description" content="<php echo $page_description; ?>" />
<!--in index.php name title...$page_title = "Home" before including this header.php page-->

<!-- Required meta tags -->
<!--To ensure proper rendering and touch zooming for all devices, add the responsive viewport meta tag-->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

<!-- Bootstrap CSS -->
<!--keep the boostrap css first in CSS list-->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous">
<style>
  /* Remove the navbar's default margin-bottom and rounded borders */ 
  .navbar {
    margin-bottom: 0;
     border-radius: 0;
  }
  /* Set black background color, white text and some padding */
  footer {
    background-color: #555;
    color: white;
    padding: 15px;
    text-align: center;
    margin-left: auto;
    margin-right: auto;
  }
</style>