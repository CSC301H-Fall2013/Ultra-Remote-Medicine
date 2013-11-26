package com.example.myapp;

import org.json.JSONException;
import org.json.JSONObject;
import com.example.myapp.R;
import android.os.Bundle;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends ActivityAPI {
	Context mContext;
	private EditText mPatientUserName;
	private EditText mPatientPassword;

	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		mContext = this;
		try {
			SharedPreferences session_id = getSharedPreferences(SESSIONID, 0);
			String session_string = session_id.getString("sessionid", null);
			if (session_string != null) {
				jsonSessionId = new JSONObject(session_string);
			} else {
				jsonSessionId = null;
			}
		} catch (JSONException e) {
			e.printStackTrace();
		}
		if (jsonSessionId != null
				&& jsonSessionId.optString("success").equals("true")) {
			Intent i = new Intent(mContext, DashboardActivity.class);
			startActivity(i);
		}
		
		Button nextButton = (Button) findViewById(R.id.login_submit);
		nextButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				mPatientUserName = (EditText) findViewById(R.id.login_username);
				mPatientPassword = (EditText) findViewById(R.id.login_password);

				Thread thread = new Thread(new Runnable() {
					@Override
					public void run() {
						try {
							// URL
							String urlString = "http://ultra-remote-medicine."
									+ "herokuapp.com/mobile/login";
							// String urlString =
							// "http://10.0.2.2:8000/mobile/login";
							String jsonString = "{\"username\": \""
									+ mPatientUserName.getText().toString()
									+ "\", \"password\": \""
									+ mPatientPassword.getText().toString()
									+ "\"}";
							jsonSessionId = communicate(urlString, jsonString);
						} catch (Exception e) {
							e.printStackTrace();
						}
					}
				});
				thread.start();
				int timer = 0;
				while (jsonSessionId == null && timer < 300) {
					try {
						Thread.sleep(200);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
					timer++;
				}
				Toast msg = Toast.makeText(getBaseContext(),
						(timer < 300 ? jsonSessionId.optString("sessionid")
								: "Server time out"), Toast.LENGTH_LONG);
				msg.show();
				msg = null;
				if (jsonSessionId != null
						&& jsonSessionId.optString("success").equals("true")) {
					SharedPreferences session_id = getSharedPreferences(
							SESSIONID, 0);
					SharedPreferences.Editor editor = session_id.edit();
					try {
						jsonSessionId.put("username", mPatientUserName
								.getText().toString());
					} catch (JSONException e) {
						e.printStackTrace();
					}
					editor.putString("sessionid", jsonSessionId.toString());
					editor.commit();
					Intent i = new Intent(mContext, DashboardActivity.class);
					startActivity(i);
				} else {
					jsonSessionId = null;
				}
			}
		});
	}
}
