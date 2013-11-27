package com.example.myapp;

import org.json.JSONObject;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class DashboardActivity extends ActivityAPI {
	Context mContext;
	private EditText mSearchKey;
	public static JSONObject jsonCheck;
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.dashboard);
        mContext = this;
        mSearchKey = (EditText) findViewById(R.id.search_box);
        TextView t = (TextView)findViewById(R.id.username_lb);
        t.setText("Welcome, " + jsonCurSessionId.optString("username"));
        
        //Add_patient button event
        Button newPatientButton = (Button) findViewById(R.id.add_new_patient_btn);
        newPatientButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
            	
            	//navigate to add new patient page
        		Intent i = new Intent(mContext, AddNewPatientActivity.class);
        		startActivity(i);
            }
        });
        
        //logout button event
        Button logoutButton = (Button) findViewById(R.id.logout_btn);
        logoutButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
            	
            	//clear the local session id info
            	SharedPreferences session_id = 
            			getSharedPreferences(MainActivity.SESSIONID, 0);
				SharedPreferences.Editor editor = session_id.edit();
				editor.putString("sessionid", null);
				editor.commit();
				
				//navigate to login page
        		Intent i = new Intent(mContext, MainActivity.class);
        		startActivity(i);
            }
        });
        
        //Add_new_case event
        Button newCaseButton = (Button) findViewById(R.id.add_new_case_btn);
        newCaseButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
            	
            	//navigate to add new case page
        		Intent i = new Intent(mContext, AddNewCaseActivity.class);
        		startActivity(i);
            }
        });
        
        //Search button click event
        Button finishButton = (Button) findViewById(R.id.search_btn);
		finishButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				jsonCurPatientId = null;
				jsonCurPatient = null;
				
				// create a new thread to upload data
				Thread thread = new Thread(new Runnable() {
					@Override
					public void run() {
						try {
							// URL
							String urlString = "view_patient";
							//Json package
							String jsonString = "{\"session_key\": \""
									+ jsonCurSessionId.optString("sessionid")
									+ "\", \"patient_id\": \""
									+ mSearchKey.getText().toString()
									+ "\"}";
							
							jsonCurPatient = communicate(urlString, jsonString);
							
						} catch (Exception e) {
							e.printStackTrace();
						}
					}
				});
				thread.start();
				
				// wait for the server respond
				int timer = 0;
				while (jsonCurPatient == null && timer < 50) {
					try {
						Thread.sleep(200);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
					timer++;
				}
				Toast msg = Toast.makeText(getBaseContext(),
						(timer < 50 ? jsonCurPatient.optString("firstName")
								: "Server time out"), Toast.LENGTH_LONG);
				msg.show();
				msg = null;
				if (jsonCurPatient != null
						&& !jsonCurPatient.optString("success").equals("false")) {
					//If server find the key, then navigate to search result page
					jsonCurPatientId = jsonCurPatient;
					Intent i = new Intent(mContext, PatientPageActivity.class);
					startActivity(i);
				} else{
					jsonCurPatient = null;
				}
				
			}
		});
    }
}
