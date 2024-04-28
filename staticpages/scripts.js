 
 // Used to check which page is currently loaded.
host = window.location.origin
 
 // Gets the query string from the search box.
  function getUserQuery(){

    var query = document.getElementById('userQuery').value

    return query
}

            // Clears the values in the product form so that it's empty for next use.
function clearQueryBox() {

    var query = document.getElementById('userQuery')

    query.value = ''

}

// Shows the table of products, and hides any customer tables on the page.
function showResults() {

    document.getElementById('result-display').style.display = "block"
}


// Fills each row of the table with the product details acquired via either of the above GET requests.
function addResultToTable(result){
    tableElem = document.getElementById("resultTable")
    rowElem = tableElem.insertRow(-1)

    cell1 = rowElem.insertCell(0)
    cell1.innerHTML = result.name

    // Making this cell an image.
    var img = document.createElement('img')
    img.width = 100
    img.height = 100
    img.src = result.image
    cell2 = rowElem.insertCell(1)
    cell2.append(img)
    }


// Makes a POST call to the app.py Flask app to run the query.
function runQuery(){

    query= getUserQuery()
    console.log(query)

    $.ajax({
        url: host,
        data:JSON.stringify(query),
        method:"POST",
        dataType:"JSON",
        contentType: "application/json; charset=utf-8",
        success:function(results){
            //populateResults(results)
            for (result of results){
                addResultToTable(result)
                }
            showResults()
            clearQueryBox()

        },
        error:function(xhr,status,error){
            console.log("error"+error)
    }
    })

}
