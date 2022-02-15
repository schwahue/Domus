// requires API_ENDPOINT_URL_STR in window scope

var
	$type_select = $("[data-role='type_select']");
	$filter_type = $("[data-role='filter_type']"),
	$property_info = $("[data-role='property_info']");

function g_ajaxer(url_str, params, ok_cb, fail_cb){
	$.ajax({
		url: url_str,
		type: "POST",
		data: JSON.stringify(params),
		crossDomain: true,
		contentType: "application/json",
		dataType: "json",
		success: ok_cb,
		error: fail_cb,
		timeout: 3000
	});
}
function clearFilter(){
	$type_select.val("All");
	$property_info.html("");
	$property_info
		.attr("data-showing", "not_showing")
	$filter_type.text("Showing all properties");
	//do new search
	postRequest("all");
}
function handleFailure(fe){
	console.log("FAIL");
	if(fe.status === 405){
		$filter_type.text("No API to call");
	}else{
		$filter_type.text("Failed due to CORS");
	}
}
function handleSuccess(data_arr){
	var 
		filter_str = $type_select.val();
	if(data_arr.length === 0){
		$filter_type.text("No " + filter_str.toLowerCase() + " properties found");
		$property_info
			.attr("data-showing", "not_showing")
	}
	showProperties(data_arr);
}
function postRequest(type_str){
	showSearching();
	var params = {
		type_str: type_str
	};
	g_ajaxer(window.API_ENDPOINT_URL_STR, params, handleSuccess, handleFailure);
}
function showProperties(data_arr){
	var 
		html_str = '',
		type_str = "",
		district_str = "",
		bedroom_str = "",
		price_str = "",
		address_str = "",
		listed_by_str = "",
		// date_str = "",
		filter_str = $type_select.val();
	for(var i_int = 0; i_int < data_arr.length; i_int += 1){
		type_str = data_arr[i_int].type.S || data_arr[i_int].type;
		district_str = data_arr[i_int].district.S || data_arr[i_int].dictrict;
		bedroom_str = data_arr[i_int].bedroom.S || data_arr[i_int].bedroom;
		price_str = data_arr[i_int].price.S || data_arr[i_int].price;
		address_str = data_arr[i_int].address.S || data_arr[i_int].address;
		listed_by_str = data_arr[i_int].listed_by.S || data_arr[i_int].listed_by;
		// date_str = new Date(data_arr[i_int].data_found.S).toLocaleDateString();
		html_str += '<article>';
		html_str += 	'<h4>' + address_str + ' : ' + type_str + '</h4>';
		// html_str += '<h5>Found:' + date_str + '</h5>';
		html_str += 	'<figure>';
		html_str += 		'<img alt="this is a picture of ' +  address_str + ' " src="images/' + address_str.toLowerCase() + '.png" width="300" height="300" />'; 
		html_str += 		'<figcaption>' + district_str + '</figcaption>';
		html_str += 	'</figure>';
		html_str += '</article>';
	}
	$filter_type.text("Showing " + filter_str.toLowerCase() + " properties");
	$property_info
		.attr("data-showing", "showing")
		.append(html_str);
	if(data_arr.length === 0){
		$property_info.html('<h6>No properties found!</h6>');
	}

}
function showSearching(){
	var 
		filter_str = $type_select.val();
	$filter_type.text("Searching database for " + filter_str.toLowerCase() + " properties...");
	$property_info.attr("data-showing", "not_showing").html("");
}
function submitType(se){
	se.preventDefault();
	//validate todo
	postRequest($type_select.val());
}

// handlers
$(document).on("change", "[data-action='choose_type']", submitType);


//onm load
postRequest("All");