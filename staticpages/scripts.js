 
 // Used to check which page is currently loaded.
host = window.location.origin
 
 // Gets the query string from the search box.
  function getUserQuery(){

    var query = document.getElementById('userQuery').value

    return query
}

// Clears the search box so that it's empty for next use.
function clearQueryBox() {

    var query = document.getElementById('userQuery')

    query.value = ''

}

// Shows the table of results
function showResults() {

    document.getElementById('result-display').style.display = "block"
}


// Fills each row of the table with the Pokemon name and images
function addResultToTable(result){
    tableElem = document.getElementById("resultTable")
    rowElem = tableElem.insertRow(-1)

    cell1 = rowElem.insertCell(0)
    cell1.innerHTML = result.name

    // Making this cell an image.
    var img = document.createElement('img')
    img.width = 100
    img.height = 100
    img.src = "https://raw.githubusercontent.com/OtherBrian/image-search-engine/main/" + result.image
    cell2 = rowElem.insertCell(1)
    cell2.append(img)
    }


// Makes a POST call to the app.py Flask app to run the query.
function runQuery(){

    // Clear any previous results
    $('#resultTable tr:not(:first)').remove();

    query= getUserQuery()

    // Send the user query to the app
    $.ajax({
        url: host,
        data:JSON.stringify(query),
        method:"POST",
        dataType:"JSON",
        contentType: "application/json; charset=utf-8",
        // Popular the results table
        success:function(results){
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
