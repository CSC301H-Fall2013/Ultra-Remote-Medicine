package com.example.myapp;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class PatientPageActivity extends ActivityAPI {
	Context mContext;

	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.patient_page);
		mContext = this;
		jsonPatient = null;

		Thread thread = new Thread(new Runnable() {
			@Override
			public void run() {
				try {
					// URL
					String urlString = "http://ultra-remote-medicine."
							+ "herokuapp.com/mobile/view_patient";
					// String urlString =
					// "http://10.0.2.2:8000/mobile/view_patient";
					String jsonString = "{\"session_key\": \""
							+ jsonSessionId.getString("sessionid")
							+ "\", \"patient_id\": \""
							+ AddNewPatientActivity.jsonPatientId
									.getString("patient_id") + "\"}";

					jsonPatient = communicate(urlString, jsonString);

				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
		thread.start();
		int timer = 0;
		while (jsonPatient == null && timer < 50) {
			try {
				Thread.sleep(200);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			timer++;
		}
		Toast msg = Toast.makeText(getBaseContext(),
				(timer < 50 ? jsonPatient.optString("firstName")
						: "Server time out"), Toast.LENGTH_LONG);
		msg.show();
		msg = null;

		Button newCaseButton = (Button) findViewById(R.id.patientpage_add_new_case_btn);
		newCaseButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				Intent i = new Intent(mContext, AddNewCaseActivity.class);
				startActivity(i);
			}
		});

		// patientpage_pre_btn
		// patientpage_next_btn

	}
}