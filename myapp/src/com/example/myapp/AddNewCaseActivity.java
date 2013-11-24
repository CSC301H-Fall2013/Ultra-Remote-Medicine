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

public class AddNewCaseActivity extends Activity {
	Context mContext;
	private EditText mPatientID;
	private EditText mPatientPriority;
	private EditText mPatientComments;
	public static JSONObject jsonCheck;
	
	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.add_new_case);
		mContext = this;
        mPatientID = (EditText) findViewById(R.id.patient_id);
        mPatientPriority = (EditText) findViewById(R.id.patient_priority);
        mPatientComments = (EditText) findViewById(R.id.patient_comments);
        
		Button finishButton = (Button) findViewById(R.id.case_finish);
		finishButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				Thread thread = new Thread(new Runnable() {
					@Override
					public void run() {
						try {
							// URL
							String urlString = "http://ultra-remote-medicine."
									+ "herokuapp.com/mobile/add_case";
							//Json package
							String jsonString = "{\"session_key\": \""
									+ MainActivity.jsonSessionId.optString("sessionid")
									+ "\", \"patient\": \""
									+ mPatientID.getText().toString()
									+ "\", \"comments\": \""
									+ mPatientComments.getText().toString()
									+ "\", \"priority\": \""
									+ mPatientPriority.getText().toString()
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