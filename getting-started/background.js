


chrome.tabs.onUpdated.addListener( function (tabId, changeInfo, tab) {

  
  // var activeTabUrl = tab.url;
  
  if (changeInfo.status == 'complete' && tab.active) {
   
    var user=""
    chrome.identity.getProfileUserInfo(function(userInfo) {
      /* Use userInfo.email, or better (for privacy) userInfo.id
         They will be empty if user is not signed in in Chrome */
         user = userInfo.email;
         
    


        console.log(user);

        var activeTabUrl = tab.url;
        

        if (tab.url.indexOf('https://www.google.com/search?q') > -1) {
        
            var myArray = activeTabUrl.split('=');
            var search_keys = myArray[1].split('&');
            var query = search_keys[0].replace(/[+_]/g, ' ');
            //then
            console.log("Tab updated! Tab URL: " + query);

            fetch("http://localhost:8000/api/?search_key=" + query + "&user_email=" + user, {
                method: "GET",
                headers: {
                
                    "Access-Control-Allow-Origin":"*",
                    "Content-Type": "text/plain",
                    
                },
            
            }).then(function(response) {
                return response.json();
            });
        }
        else{

            fetch("http://localhost:8000/api/update/?url_value=" + activeTabUrl, {
                method: "GET",
                headers: {
                
                    "Access-Control-Allow-Origin":"*",
                    "Content-Type": "text/plain",
                    
                },
            
            }).then(function(response) {
                return response.json();
            });

        }
    
     
    });
  }

});