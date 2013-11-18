//js module for pagination

var context;
var old_page = 1;

function Pager(tableName, itemsPerPage) {
    context = this;
    this.tableName = tableName;
    this.itemsPerPage = itemsPerPage;
    currentPage = 1;
    this.pages = 0;
    this.records;
    
    /*
    display specific records in a table row 
    */
    this.showRecords = function(from, to) {        
        var rows = document.getElementById(tableName).rows;
        // i starts from 1 to skip table header row
        for (var i = 0; i < rows.length; i++) {
            if (i < from || i > to)  
                rows[i].style.display = 'none';
            else
                rows[i].style.display = '';
        }
    }
    
    /*
    set style for old page anchor and new page anchor
    and get the range of list items to be shown for selected page
    */
    this.showPage = function(pageNumber) {
        var oldPageAnchor = document.getElementById('pg'+old_page);
        oldPageAnchor.style.textDecoration = 'none';
        oldPageAnchor.style.fontWeight = "normal";
        
        currentPage = pageNumber;
        var newPageAnchor = document.getElementById('pg'+currentPage);
        newPageAnchor.style.textDecoration = 'underline';
        newPageAnchor.style.fontWeight = "bold";
        
        var from = (pageNumber - 1) * itemsPerPage;
        var to = from + itemsPerPage - 1;
        this.showRecords(from, to);
        old_page = currentPage;
    }       
    
    /*
    get the total no of records and no of pages to be displayed 
    */
    this.init = function() {
        var rows = document.getElementById(tableName).rows;
        this.records = (rows.length);
        this.pages = Math.ceil(this.records / itemsPerPage);
    }
	
    /*
    show page navigator
    */
    this.showPageNav = function() {
        var ul = document.getElementById("unordered-list");
        
        //add PREV link and set click event
        var prev = document.createElement('li');
    	ul.appendChild(prev);
    	prev.innerHTML="<a class='pg-normal' style='cursor:hand; cursor:pointer;'>Prev</a>";
    	prev.addEventListener("click", function (){
    		if (currentPage >= 2){
            		context.showPage(currentPage - 1);
            	}else{
            		//unfocus prev link from here when it comes to the first page
            	}
    	} );
    	
    	//add pages links and set click event to display list in table row depending
    	//upon selected page
    	for (var page = 1; page <= 3; page++) {
		var page_number = document.createElement('li');
		page_number.innerHTML="<a id='pg" + page + "' class='pg-normal' onclick='pager.showPage(" + page + ");' style='cursor:hand; cursor:pointer;' >"+page+"</a>";
    		
		ul.appendChild(page_number);
		
	}
    	
    	//add NEXT link and set click event
    	var next = document.createElement('li');
    	ul.appendChild(next);
    	next.innerHTML="<a class='pg-normal' style='cursor:hand; cursor:pointer;'>Next</a>";
    	next.addEventListener("click", function (){
    		if (currentPage >= 1 && currentPage+1 <= context.pages){
            		context.showPage(currentPage + 1);
            	}else{
            		//unfocus next link from here when it comes to the last page
            	}
    	});
    	
    	
    	
    }
}

