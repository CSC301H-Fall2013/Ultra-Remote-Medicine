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
		mPatientUserName = (EditText) findViewById(R.id.login_username);
		mPatientPassword = (EditText) findViewById(R.id.login_password);

		// read session id from local data storage
		try {
			SharedPreferences session_id = getSharedPreferences(SESSIONID, 0);
			String session_string = session_id.getString("sessionid", null);
			if (session_string != null) {
				jsonCurSessionId = new JSONObject(session_string);
			} else {
				jsonCurSessionId = null;
			}
		} catch (JSONException e) {
			e.printStackTrace();
		}
		if (jsonCurSessionId != null
				&& jsonCurSessionId.optString("success").equals("true")) {
			Intent i = new Intent(mContext, DashboardActivity.class);
			startActivity(i);
		}

		// Login Button Click event to login to the server
		Button nextButton = (Button) findViewById(R.id.login_submit);
		nextButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {

				jsonCurSessionId = null;

				// create a new thread to login the to server
				Thread thread = new Thread(new Runnable() {
					@Override
					public void run() {
						try {
							// URL
							String urlString = "login";
							// Json package string
							String jsonString = "{\"username\": \""
									+ mPatientUserName.getText().toString()
									+ "\", \"password\": \""
									+ mPatientPassword.getText().toString()
									+ "\"}";
							jsonCurSessionId = communicate(urlString,
									jsonString);
						} catch (Exception e) {
							e.printStackTrace();
						}
					}
				});
				thread.start();

				// wait for the server respond
				int timer = 0;
				while (jsonCurSessionId == null && timer < 300) {
					try {
						Thread.sleep(200);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
					timer++;
				}
				if (timer >= 300
						|| jsonCurSessionId.optString("success")
								.equals("false")) {
					String msgString = (timer < 300 ? "Fail to login"
							: "Server time out");
					Toast msg = Toast.makeText(getBaseContext(), msgString,
							Toast.LENGTH_LONG);
					msg.show();
					msg = null;
				}
				if (jsonCurSessionId != null
						&& jsonCurSessionId.optString("success").equals("true")) {

					// if login successfully, stores the session id to local
					// storage
					SharedPreferences session_id = getSharedPreferences(
							SESSIONID, 0);
					SharedPreferences.Editor editor = session_id.edit();
					try {
						jsonCurSessionId.put("username", mPatientUserName
								.getText().toString());
					} catch (JSONException e) {
						e.printStackTrace();
					}
					editor.putString("sessionid", jsonCurSessionId.toString());
					editor.commit();

					// navigate to dash board
					Intent i = new Intent(mContext, DashboardActivity.class);
					startActivity(i);
				} else {
					jsonCurSessionId = null;
				}
			}
		});
	}
}
