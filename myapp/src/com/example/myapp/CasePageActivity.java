package com.example.myapp;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.Toast;

public class CasePageActivity extends ActivityAPI {
	Context mContext;
	private TextView cCaseId;
	private TextView cPatientName;
	private TextView cPatientUrmId;
	private TextView cPatientDob;
	private TextView cPatientHealthId;
	private TextView cPatientSex;
	private TextView cCasePriority;

	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.case_page);
		mContext = this;
		cCaseId = (TextView) findViewById(R.id.casepage_caseid);
		cPatientName = (TextView) findViewById(R.id.casepage_patient_name);
		cPatientUrmId = (TextView) findViewById(R.id.casepage_patient_urmid);
		cPatientDob = (TextView) findViewById(R.id.casepage_patient_dob);
		cPatientHealthId = (TextView) findViewById(R.id.casepage_patient_health_id);
		cPatientSex = (TextView) findViewById(R.id.casepage_patient_sex);
		cCasePriority = (TextView) findViewById(R.id.casepage_case_priority);

		loadCaseInfo();

	}

	private void loadCaseInfo() {
		cCaseId.setText("Case: ");
		cPatientName.setText("Name: ");
		cPatientUrmId.setText("URM ID: ");
		cPatientDob.setText("DOB: ");
		cPatientHealthId.setText("Health ID: ");
		cPatientSex.setText("Sex: ");
		cCasePriority.setText("Priority: ");

		if (jsonCurCase == null) {
			if (jsonCurCaseId != null) {
				// Create a new thread to load patient data
				Thread thread = new Thread(new Runnable() {
					@Override
					public void run() {
						try {
							// URL
							String urlString = "view_case";
							// Json package string
							String jsonString = "{\"session_key\": \""
									+ jsonCurSessionId.getString("sessionid")
									+ "\", \"case_id\": \""
									+ jsonCurCaseId.getString("case_id")
									+ "\"}";

							jsonCurCase = communicate(urlString, jsonString);

						} catch (Exception e) {
							e.printStackTrace();
						}
					}
				});
				thread.start();

				// wait for the server respond
				int timer = 0;
				while (jsonCurCase == null && timer < 50) {
					try {
						Thread.sleep(200);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
					timer++;
				}
				Toast msg = Toast.makeText(getBaseContext(),
						(timer < 50 ? jsonCurCase.optString("firstName")
								: "Server time out"), Toast.LENGTH_LONG);
				msg.show();
				msg = null;
				if (jsonCurCase == null
						|| jsonCurCase.optString("success").equals("false")) {
					// If server can not find the key, then navigate to dash
					// board
					jsonCurCase = null;

					Intent i = new Intent(mContext, DashboardActivity.class);
					startActivity(i);
				}
			} else {
				Intent i = new Intent(mContext, DashboardActivity.class);
				startActivity(i);
			}
		}
		if (jsonCurCase != null){
			cCaseId.setText("Case: " + jsonCurCase.optString("case_id"));
			cPatientName.setText("Name: " + jsonCurCase.optString("lastName") + ", " + jsonCurCase.optString("firstName"));
			cPatientUrmId.setText("URM ID: " + jsonCurCase.optString("patient_id"));
			cPatientDob.setText("DOB: " + jsonCurCase.optString("date_of_birth"));
			cPatientHealthId.setText("Health ID: " + jsonCurCase.optString("health_id"));
			cPatientSex.setText("Sex: " + jsonCurCase.optString("gender"));
			cCasePriority.setText("Priority: " + jsonCurCase.optString("priority"));
		}
	}
}
