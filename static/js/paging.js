// JS module for pagination

var context;
var package_context;
var bundle_context;

function Pager(tableName, itemsPerPage, listID) {
    context = this;
    this.tableName = tableName;
    this.listID = listID;
    this.itemsPerPage = itemsPerPage;
    this.pages = 0;
    this.records;
    this.next_counter = 3;
    this.old_page = 1;
    this.currentPage = 1;
    
    //code before paging
    init(tableName, context);
    //show page navigator
    showPageNav(tableName, context, listID, 'c'); 
    //show page
    showPage(1, tableName);
}

function Packages(tableName, itemsPerPage, listID) {
    package_context = this;
    this.tableName = tableName;
    this.listID = listID;
    this.itemsPerPage = itemsPerPage;
    this.pages = 0;
    this.records;
    this.next_counter = 3;
    this.old_page = 1;
    this.currentPage = 1;
    
    //code before paging
    init(tableName, package_context);
    //show page navigator
    showPageNav(tableName, package_context, listID, 'p'); 
    //show page
    showPage(1, tableName);
}

function Bundles(tableName, itemsPerPage, listID) {
    bundle_context = this;
    this.tableName = tableName;
    this.listID = listID;
    this.itemsPerPage = itemsPerPage;
    this.pages = 0;
    this.records;
    this.next_counter = 3;
    this.old_page = 1;
    this.currentPage = 1;
    
    //code before paging
    init(tableName, bundle_context);
    //show page navigator
    showPageNav(tableName, bundle_context, listID, 'b'); 
    //show page
    showPage(1, tableName);
}


/*
    get the total no of records and no of pages to be displayed 
    */
    function init(table, cont) {
        var rows = document.getElementById(table).rows;
        cont.records = (rows.length);
        cont.pages = Math.ceil(cont.records / cont.itemsPerPage);
    }
    
    /*
    display specific records in a table row 
    */
    function showRecords(from, to, tableName) {   
    	try{
    		var rows = document.getElementById(tableName).rows;
    	}
    	catch(err){
    		var rows = document.getElementById(tableName.id).rows;
    	}   
    
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
    function showPage(pageNumber, tableName) {
    	var cont;
    	var id_extension;
    	
	if(tableName == 'code'){
		cont = context;
		id_extension = 'c';
	}else if(tableName.id == 'code'){
		cont = context;
		id_extension = 'c';
	}else if(tableName == 'package'){
		cont = package_context;
		id_extension = 'p';
	}else if(tableName.id == 'package'){
		cont = package_context;
		id_extension = 'p';
	}else if(tableName == 'bundle'){
		cont = bundle_context;
		id_extension = 'b';
	}else if(tableName.id == 'bundle'){
		cont = bundle_context;
		id_extension = 'b';
	}
    	   
        var oldPageAnchor = document.getElementById('pg'+id_extension+cont.old_page);
        oldPageAnchor.style.textDecoration = 'none';	
        oldPageAnchor.style.fontWeight = "normal";
        
        cont.currentPage = pageNumber;
        var newPageAnchor = document.getElementById('pg'+id_extension+cont.currentPage);
        newPageAnchor.style.textDecoration = 'underline';
        newPageAnchor.style.fontWeight = "bold";
        
        cont.old_page = cont.currentPage;
        
        var from = (pageNumber - 1) * cont.itemsPerPage; //need to add context.itemsperpage
        var to = from + cont.itemsPerPage - 1; //need to add context.itemsperpage
        showRecords(from, to, tableName);
        
    }       
	
    /*
    show page navigator
    */
    function showPageNav(tableName, cont, listID, id_extension) {
        var ul = document.getElementById(listID);
        
        //add PREV link and set click event
        var prev = document.createElement('li');
    	ul.appendChild(prev);
    	prev.innerHTML="<a class='pg-normal' style='cursor:hand; cursor:pointer;'> << </a>";
    	prev.addEventListener("click", function (){
    		try
  		{
	    		if (cont.currentPage > 1){
	    			//display page which is visible in the navigator
	    			showPage((cont.currentPage - 1),tableName);
		    	}
            	}
		catch(err)
 	 	{
 	 		//when we are trying to view previous page which is not 
 	 		//visible in the navigator add that page link in the navigator 
 	 		//remove the extreme right page link
 	 		var page_number = document.createElement('li');
 	 		
	    		page_number.innerHTML="<a id='pg"+id_extension + (cont.currentPage) + "' class='pg-normal' onclick='showPage("+cont.currentPage+","+tableName+");' style='cursor:hand; cursor:pointer;' >"+(cont.currentPage)+"</a>";
	    			
    			//remove extreme right link page from navigator
			$('#pg'+id_extension+(cont.currentPage+3)).remove();
		    	
			//add new link to the left of navigator
			$('#'+listID+' li:eq(1)').after(page_number);
			
			//show page
			showPage((cont.currentPage), tableName);
			
 	 		
 	 	}
    	} );
    	
    	//add pages links and set click event to display list in table row depending
    	//upon selected page
    	var count = 3;
    	if(cont.pages == 2 ){
    		count = 2;
    	}else if(cont.pages == 1){
    		count = 1;
    	}
    	
    	for (var page = 1; page <= count; page++) {
    		
		var page_number = document.createElement('li');
		
    		page_number.innerHTML="<a id='pg"+id_extension + page + "' class='pg-normal' onclick='showPage(" +page+","+tableName+ ");' style='cursor:hand; cursor:pointer;' >"+page+"</a>";
		ul.appendChild(page_number);
		
	}
    	
    	//add NEXT link and set click event
    	var next = document.createElement('li');
    	ul.appendChild(next);
    	next.innerHTML="<a class='pg-normal' style='cursor:hand; cursor:pointer;'> >> </a>";
    	next.addEventListener("click", function (){
    		try
  		{
  			//add next page which is not viewed before
	    		if (cont.currentPage < cont.pages){
	    			//show page
				showPage((cont.currentPage + 1),tableName);
		    	}
            	}
		catch(err)
 	 	{
 	 		//when we are trying to view next page which is added before but not 
 	 		//visible in the navigator, add that page link in the navigator 
 	 		//remove the extreme left page link
	    		var page_number = document.createElement('li');
	    		
	    		
	    		page_number.innerHTML="<a id='pg"+id_extension + (cont.currentPage) + "' class='pg-normal' onclick='showPage(" +cont.currentPage+","+tableName+");' style='cursor:hand; cursor:pointer;' >"+(cont.currentPage)+"</a>";
	    		
    			//remove prev link(extreme left)
			$('#pg'+id_extension+(cont.currentPage-3)).remove();
		    	
		    	
			//add new link to the right of the navigator
			$('#'+listID+' li:eq('+cont.next_counter+')').after(page_number);
			
			cont.next_counter++;
			
			//show page
			showPage(cont.currentPage, tableName);
 	 	}
    		
    	});
    }
