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
		TextView t = (TextView) findViewById(R.id.username_lb);
		t.setText("Welcome, " + jsonCurSessionId.optString("username"));

		// Add_patient button event
		Button newPatientButton = (Button) findViewById(R.id.add_new_patient_btn);
		newPatientButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {

				jsonCurSearchList = null;
				jsonCurPatientId = null;
				jsonCurPatient = null;
				jsonCurCaseList = null;
				jsonCurCaseId = null;
				jsonCurCase = null;
				
				// navigate to add new patient page
				Intent i = new Intent(mContext, AddNewPatientActivity.class);
				startActivity(i);
			}
		});

		// logout button event
		Button logoutButton = (Button) findViewById(R.id.logout_btn);
		logoutButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {

				// clear the local session id info
				SharedPreferences session_id = getSharedPreferences(
						MainActivity.SESSIONID, 0);
				SharedPreferences.Editor editor = session_id.edit();
				editor.putString("sessionid", null);
				editor.commit();

				jsonCurSessionId = null;
				jsonCurSearchList = null;
				jsonCurPatientId = null;
				jsonCurPatient = null;
				jsonCurCaseList = null;
				jsonCurCaseId = null;
				jsonCurCase = null;

				// navigate to login page
				Intent i = new Intent(mContext, MainActivity.class);
				startActivity(i);
			}
		});

		// new_case button click event
		Button searchIdButton = (Button) findViewById(R.id.add_new_case_btn);
		searchIdButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {

				jsonCurSearchList = null;
				jsonCurPatientId = null;
				jsonCurPatient = null;
				jsonCurCaseList = null;
				jsonCurCaseId = null;
				jsonCurCase = null;

				// create a new thread to upload data
				Thread thread = new Thread(new Runnable() {
					@Override
					public void run() {
						try {
							// URL
							String urlString = "view_patient";
							// Json package
							String jsonString = "{\"session_key\": \""
									+ jsonCurSessionId.optString("sessionid")
									+ "\", \"patient_id\": \""
									+ mSearchKey.getText().toString() + "\"}";

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
					// If server find the key, then navigate to search result
					// page
					jsonCurPatientId = jsonCurPatient;
					Intent i = new Intent(mContext, PatientPageActivity.class);
					startActivity(i);
				} else {
					jsonCurPatient = null;
				}

			}
		});
		
		
		// Search button click event
		Button searchButton = (Button) findViewById(R.id.search_btn);
		searchButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {

				jsonCurSearchList = null;
				jsonCurPatientId = null;
				jsonCurPatient = null;
				jsonCurCaseList = null;
				jsonCurCaseId = null;
				jsonCurCase = null;

				// create a new thread to upload data
				Thread thread = new Thread(new Runnable() {
					@Override
					public void run() {
						try {
							// URL
							String urlString = "search";
							// Json package
							String jsonString = "{\"session_key\": \""
									+ jsonCurSessionId.optString("sessionid")
									+ "\", \"q\": \""
									+ mSearchKey.getText().toString() + "\"}";

							jsonCurSearchList = communicate(urlString, jsonString);

						} catch (Exception e) {
							e.printStackTrace();
						}
					}
				});
				thread.start();

				// wait for the server respond
				int timer = 0;
				while (jsonCurSearchList == null && timer < 50) {
					try {
						Thread.sleep(200);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
					timer++;
				}
				Toast msg = Toast.makeText(getBaseContext(),
						(timer < 50 ? jsonCurSearchList.optString("success")
								: "Server time out"), Toast.LENGTH_LONG);
				msg.show();
				msg = null;
				if (jsonCurSearchList != null
						&& !jsonCurSearchList.optString("success").equals("false")) {
					// If server find the key, then navigate to search result
					// page
					Intent i = new Intent(mContext, SearchResultActivity.class);
					startActivity(i);
				} else {
					jsonCurSearchList = null;
				}

			}
		});
	}
}
