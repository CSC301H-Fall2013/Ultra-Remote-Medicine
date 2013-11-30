package com.example.myapp;

import com.example.myapp.R;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

public class AddNewPatientActivity extends ActivityAPI {
	Context mContext;
	private EditText mPatientFirstName;
	private EditText mPatientLastName;
	private Spinner mPatientSex;
	private EditText mPatientDOB;
	private EditText mPatientHealthID;
	private EditText mPatientGPSCoordinates;
	private EditText mPatientAddress;
	private EditText mPatientPhoneNumber;
	private EditText mPatientEmail;

	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.add_new_patient);
		mContext = this;
		mPatientFirstName = (EditText) findViewById(R.id.patient_first_name);
		mPatientLastName = (EditText) findViewById(R.id.patient_last_name);
		mPatientSex = (Spinner) findViewById(R.id.patient_sex);
		mPatientDOB = (EditText) findViewById(R.id.patient_dob);
		mPatientHealthID = (EditText) findViewById(R.id.patient_health_id);
		mPatientGPSCoordinates = (EditText) findViewById(R.id.patient_gps_coordinates);
		mPatientAddress = (EditText) findViewById(R.id.patient_address);
		mPatientPhoneNumber = (EditText) findViewById(R.id.patient_phone_number);
		mPatientEmail = (EditText) findViewById(R.id.patient_email);

		// Send Button Click event to upload data to the server
		Button finshButton = (Button) findViewById(R.id.patient_finish);
		finshButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {

				jsonCurPatientId = null;

				// create a new thread to upload data
				Thread thread = new Thread(new Runnable() {
					@Override
					public void run() {
						try {
							// URL
							String urlString = "add_patient";
							// Json package string
							String jsonString = "{\"session_key\": \""
									+ MainActivity.jsonCurSessionId
											.getString("sessionid")
									+ "\", \"first_name\": \""
									+ mPatientFirstName.getText().toString()
									+ "\", \"last_name\": \""
									+ mPatientLastName.getText().toString()
									+ "\", \"gps_coordinates\": \""
									+ mPatientGPSCoordinates.getText()
											.toString() + "\", \"address\": \""
									+ mPatientAddress.getText().toString()
									+ "\", \"date_of_birth\": \""
									+ mPatientDOB.getText().toString()
									+ "\", \"phone_number\": \""
									+ mPatientPhoneNumber.getText().toString()
									+ "\", \"health_id\": \""
									+ mPatientHealthID.getText().toString()
									+ "\", \"photo_link\": \"" + ""
									+ "\", \"sex\": \""
									+ mPatientSex.getSelectedItem().toString()
									+ "\", \"email\": \""
									+ mPatientEmail.getText().toString()
									+ "\"}";

							jsonCurPatientId = communicate(urlString,
									jsonString);

						} catch (Exception e) {
							e.printStackTrace();
						}
					}
				});
				thread.start();

				// wait for the server respond
				int timer = 0;
				while (jsonCurPatientId == null && timer < 300) {
					try {
						Thread.sleep(200);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
					timer++;
				}
				if (timer >= 300
						|| (jsonCurPatientId.optString("success")
								.equals("false"))) {
					String msgString = (timer < 300 ? "Fail to create patient"
							: "Server time out");
					Toast msg = Toast.makeText(getBaseContext(), msgString,
							Toast.LENGTH_LONG);
					msg.show();
					msg = null;
				}
				if (jsonCurPatientId != null
						&& jsonCurPatientId.optString("success").equals("true")) {
					// If the patient created, then navigate to Patient Page
					Intent i = new Intent(mContext, PatientPageActivity.class);
					startActivity(i);
				} else {
					jsonCurPatientId = null;
				}
			}
		});
	}
}
