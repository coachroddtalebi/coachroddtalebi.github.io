<!--template from: https://v4-alpha.getbootstrap.com/getting-started/introduction/-->
<!--HOW TO USE PHP AND HTML: http://www.apaddedcell.com/how-automatically-include-your-header-navigation-and-footer-every-page -->

<!--define php input variables-->
$page_title = "Home";
$page_description = "Description of this page";


<!DOCTYPE html>
<!--Bootstrap requires the use of the HTML5 doctype-->
<html lang="en">
  <head>
    $page_title = "Home";
    $page_description = "Description of this page";
    <?php include 'header.php'); ?>

    <style>
      /* Set height of the grid so .sidenav can be 100% (adjust as needed) */
      .row.content {height: 450px}
      /* Set gray background color and 100% height */
      .sidenav {
        padding-top: 20px;
        background-color: #f1f1f1;
        height: 100%;}
      /* On small screens, set height to 'auto' for sidenav and grid */
      @media screen and (max-width: 767px) {
        .sidenav {
          height: auto;
          padding: 15px;}
        .row.content {height:auto;} 
      }
    </style>
  </head>


  <body>
    <!--navigation bar-->
    <?php include 'navbar.php'); ?>

    <!--banner content-->
    <div class="container-fluid text-center">    
      <div class="row content">
        <div class="col-sm-2 sidenav" id="sidebar">
          <p>let's not put anything here</p>
        </div>

        <div class="col-sm-8 text-left" id="banner">
          <p>Intro Banner Below</p>
          <!-- Page Header -->
          <!-- Set your background image for this header on the line below. -->
          <header class="intro-header" style="background-image: url('img/about-bg.jpg')">
              <div class="container">
                  <div class="row">
                      <div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
                          <div class="page-heading">
                              <h1>Georgia Tech Crew</h1>
                              <hr class="small">
                              <span class="subheading">In Rodd We Trust.</span>
                          </div>
                      </div>
                  </div>
              </div>
          </header>
        </div>
      </div>
    </div>

    <!--google calendar embed-->
    <div id="calendar">
      <iframe src="https://calendar.google.com/calendar/embed?showTitle=0&amp;showPrint=0&amp;showTabs=0&amp;showCalendars=0&amp;height=600&amp;wkst=1&amp;bgcolor=%23ffffff&amp;ctz=America%2FNew_York" style="border-width:0" width="800" height="600" frameborder="0" scrolling="no"></iframe>
    </div>

    <!--weather-->
    <div id="weather">
      <h1 class="text-left">Today's Weather</h1>
      <iframe id="forecast_embed" type="text/html" frameborder="0" height="245" width="100%" src=" http://forecast.io/embed/#lat=34.0073&lon=-84.3435&name=GT Boathouse&color=#00aaff&font=Georgia&units=us12"></iframe>
      <iframe height="1000" width="100%" src="https://darksky.net/forecast/34.0073,-84.3435/us12/en"></iframe>
    </div>

    <!--footer-->
    <?php include 'footer.php'); ?>
  </body>
</html>