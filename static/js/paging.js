/*
js module for paging
*/

function Pager(tableName, itemsPerPage) {
    this.count = 0;
    this.tableName = tableName;
    this.itemsPerPage = itemsPerPage;
    this.currentPage = 1;
    this.pages = 0;
    this.inited = false;
    this.records;
    
    /*
    show list items in a table row
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
    find out the range of items to be displayed for particular page number
    and call a css class for selected page number from navigator
    */
    this.showPage = function(pageNumber) {
    	
    	if (! this.inited) {
    		alert("not inited");
    		return;
    	}
    	
        var oldPageAnchor = document.getElementById('pg'+pageNumber);
        oldPageAnchor.className = 'pg-normal';
        
        this.currentPage = pageNumber;
        var newPageAnchor = document.getElementById('pg'+this.currentPage);
        newPageAnchor.className = 'pg-selected';
        
        var from = (pageNumber - 1) * itemsPerPage;
        var to = from + itemsPerPage - 1;
        this.showRecords(from, to);
    }   
    
    /*
    previous button to display the prev 3 pages and reset the navigator accordigly
    */
    this.prev = function() {
        this.count = this.count - 3;
        if(this.count >= 0){
		if (this.currentPage < this.pages) {
		    	var from = ((this.count+1) - 1) * itemsPerPage + 1;
			var to = from + itemsPerPage - 1;
			this.showRecords(from, to);
		}
		
		var element = document.getElementById("pageNavPosition");
	    	
	    	var pagerHtml = '<span onclick="' + "pager" + '.prev();" class="pg-normal"> &#171 Prev </span> | ';
		for (var page = this.count+1; page <= this.count+3; page++) 
		    pagerHtml += '<span id="pg' + page + '" class="pg-normal" onclick="' + "pager" + '.showPage(' + page + ');">' + page + '</span> | ';
		pagerHtml += '<span onclick="'+"pager"+'.next();" class="pg-normal"> Next &#187;</span>';            
		
		element.innerHTML = pagerHtml;
        }else{
        	this.count = 0;
        }
    }
    
    /*
    next button to display the next 3 pages and reset the navigator accordigly
    */
    this.next = function() {
    	var endFlag = false;
    	this.count = this.count + 3;
        if (this.currentPage < this.pages) {
            	var from = ((this.count+1) - 1) * itemsPerPage + 1;
        	var to = from + itemsPerPage - 1;
        	this.showRecords(from, to);
        }
        var element = document.getElementById("pageNavPosition");
        var pagerHtml = '<span onclick="' + "pager" + '.prev();" class="pg-normal"> &#171 Prev </span> | ';
        for(var every_page = this.count+1; every_page <= this.count+3; every_page++){
        	
        	pagerHtml += '<span id="pg' + every_page + '" class="pg-normal" onclick="' + "pager" + '.showPage('+ every_page + ');">';
        	if(this.records >= (every_page * 10)-9){
        		//alert(this.records+" " + every_page + " " + this.records % every_page);
			pagerHtml += every_page + '</span> | ';
		}else{
			endFlag = true;
		}
        }
        if(endFlag == false){
        	pagerHtml += '<span onclick="'+"pager"+'.next();" class="pg-normal"> Next &#187;</span>';            
        }
        element.innerHTML = pagerHtml;
    }                        
    
    /*
    get the total items from table rows and total pages to be display 
    */
    this.init = function() {
        var rows = document.getElementById(tableName).rows;
        this.records = (rows.length);
        this.pages = Math.ceil(this.records / itemsPerPage);
        this.inited = true;
    }

    /*
    show page navigator
    */
    this.showPageNav = function(pagerName, positionId) {
    	if (! this.inited) {
    		alert("not inited");
    		return;
    	}
    	var element = document.getElementById(positionId);
    	
    	var pagerHtml = '<span onclick="' + pagerName + '.prev();" class="pg-normal"> &#171 Prev </span> | ';
        for (var page = 1; page <= 3; page++) 
            pagerHtml += '<span id="pg' + page + '" class="pg-normal" onclick="' + pagerName + '.showPage(' + page + ');">' + page + '</span> | ';
        pagerHtml += '<span onclick="'+pagerName+'.next();" class="pg-normal"> Next &#187;</span>';            
        
        element.innerHTML = pagerHtml;
    }
}

