/*
	Copyright @2019 [Amazon Web Services] [AWS]

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	    http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.
*/
var
    AWS = require("aws-sdk"),
    DDB = new AWS.DynamoDB({
        apiVersion: "2012-08-10",
        region: "us-east-1"
    }),
    PROPERTY_DATA_ARR = require("../../Terraform/db_functions/property_data.json");

	function addNewItemsFromJSON(){
		console.log("All items now removed, re-seeding now");
		var 
			property = {},
			property_formatted_arr = [],
			params = {};
	
	
		for(var i_int = 0; i_int < PROPERTY_DATA_ARR.length; i_int += 1){
			property = {
				PutRequest: {
					Item: {
						type: {
							"S": PROPERTY_DATA_ARR[i_int].type_str
						},
						district: {
							"S": PROPERTY_DATA_ARR[i_int].district_str
						},
						bedroom: {
							"S": PROPERTY_DATA_ARR[i_int].bedroom_str
						},
						price: {
							"S": PROPERTY_DATA_ARR[i_int].price_str
						},
						address: {
							"S": PROPERTY_DATA_ARR[i_int].address_str
						},
						listed_by: {
							"S": PROPERTY_DATA_ARR[i_int].listed_by_str
						}
					}
				}
			};
			property_formatted_arr.push(property);
		}
		params = {
			RequestItems: {
				"listings": property_formatted_arr.reverse()
			}
		};
		DDB.batchWriteItem(params, function(err, data){   
			if(err){
				throw err;
			}
			console.log("OK");         
		});
	}
	
	function init(){
		removeExistingItemsFromDynamo(function(err, data){
			if(err){
				throw err;
			} 
			addNewItemsFromJSON();
		});
	}
	
	function removeExistingItemsFromDynamo(cb){
		var 
			params = {
				RequestItems: {
					"listings": [{
						DeleteRequest: {
							Key: {
								address: {
									"S": "Yishun Ave 2 Block 166"
								}
							}
						}
					},{
						DeleteRequest: {
							Key: {
								address: {
									"S": "40 Springside Link"
								}
							}
						}
					}]
				}
			};
		   
		DDB.batchWriteItem(params, function(err, data){
			if(err){
				throw err;
			}
			//if empty table this will still work.
			//if you run into problems manaully delete the items (not the DB)
			//then run this script
			cb(null, true);
		});
	}
	
	init();