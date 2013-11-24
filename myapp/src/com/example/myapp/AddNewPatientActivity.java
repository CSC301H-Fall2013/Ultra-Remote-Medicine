package com.example.myapp;

import org.json.JSONObject;
import com.example.myapp.R;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class AddNewPatientActivity extends Activity {
	Context mContext;
	private EditText mPatientFirstName;
	private EditText mPatientLastName;
	private EditText mPatientSex;
	private EditText mPatientDOB;
	private EditText mPatientHealthID;
	private EditText mPatientGPSCoordinates;
	private EditText mPatientAddress;
	private EditText mPatientPhoneNumber;
	private EditText mPatientEmail;
	public static JSONObject jsonCheck;
		
	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.add_new_patient);
	    mContext = this;
        mPatientFirstName = (EditText) findViewById(R.id.patient_first_name);
        mPatientLastName = (EditText) findViewById(R.id.patient_last_name);
        mPatientSex = (EditText) findViewById(R.id.patient_sex);
        mPatientDOB = (EditText) findViewById(R.id.patient_dob);
        mPatientHealthID = (EditText) findViewById(R.id.patient_health_id);
        mPatientGPSCoordinates = (EditText) findViewById(R.id.patient_gps_coordinates);
        mPatientAddress = (EditText) findViewById(R.id.patient_address);
        mPatientPhoneNumber = (EditText) findViewById(R.id.patient_phone_number);
        mPatientEmail = (EditText) findViewById(R.id.patient_email);
	    
		Button finshButton = (Button) findViewById(R.id.patient_finish);
		finshButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				Thread thread = new Thread(new Runnable() {
					@Override
					public void run() {
						try {
							// URL
							String urlString = "http://ultra-remote-medicine."
									+ "herokuapp.com/mobile/add_patient";
							String jsonString = "{\"session_key\": \""
									+ MainActivity.jsonSessionId.optString("sessionid")
									+ "\", \"first_name\": \""
									+ mPatientFirstName.getText().toString()
									+ "\", \"last_name\": \""
									+ mPatientLastName.getText().toString()
									+ "\", \"gps_coordinates\": \""
									+ mPatientGPSCoordinates.getText().toString()
									+ "\", \"address\": \""
									+ mPatientAddress.getText().toString()
									+ "\", \"date_of_birth\": \""
									+ mPatientDOB.getText().toString()
									+ "\", \"phone_number\": \""
									+ mPatientPhoneNumber.getText().toString()
									+ "\", \"health_id\": \""
									+ mPatientHealthID.getText().toString()
									+ "\", \"photo_link\": \""
									+ ""
									+ "\", \"sex\": \""
									+ mPatientSex.getText().toString()
									+ "\", \"email\": \""
									+ mPatientEmail.getText().toString()
									+ "\"}";
							
							jsonCheck = MainActivity.communicate(urlString, jsonString);
							
						} catch (Exception e) {
							e.printStackTrace();
						}
					}
				});
				thread.start();
				int timer = 0;
				while (jsonCheck == null && timer < 50) {
					try {
						Thread.sleep(200);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
					timer++;
				}
				Toast msg = Toast.makeText(getBaseContext(),
						(timer < 50 ? jsonCheck.optString("type")
								: "Server time out"), Toast.LENGTH_LONG);
				msg.show();
				msg = null;
				if (jsonCheck != null) {
					Intent i = new Intent(mContext, DashboardActivity.class);
					startActivity(i);
				}
				jsonCheck = null;
			}
		});
	}
}
