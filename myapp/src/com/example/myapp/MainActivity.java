package com.example.myapp;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import org.json.JSONException;
import org.json.JSONObject;
import com.example.myapp.R;
import android.os.Bundle;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends Activity {
	Context mContext;
	private EditText mPatientUserName;
	private EditText mPatientPassword;
	public static JSONObject jsonSessionId;
	public static final String SESSIONID = "SessionId";

	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		mContext = this;
		try {
			SharedPreferences session_id = getSharedPreferences(SESSIONID, 0);
			String session_string = session_id.getString("sessionid", null);
			if (session_string != null){
				jsonSessionId = new JSONObject(session_string);
			} else{
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
					public void run(){
						try {
							// URL
							String urlString = "http://ultra-remote-medicine."
									+ "herokuapp.com/mobile/login";
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
						(timer < 300 ? jsonSessionId.optString("success")
								: "Server time out"), Toast.LENGTH_LONG);
				msg.show();
				msg = null;
				if (jsonSessionId != null
						&& jsonSessionId.optString("success").equals("true")) {
					SharedPreferences session_id = getSharedPreferences(SESSIONID, 0);
					SharedPreferences.Editor editor = session_id.edit();
					try {
						jsonSessionId.put("username", mPatientUserName.getText().toString());
					} catch (JSONException e) {
						e.printStackTrace();
					}
					editor.putString("sessionid", jsonSessionId.toString());
					editor.commit();
					Intent i = new Intent(mContext, DashboardActivity.class);
					startActivity(i);
				}else{
					jsonSessionId = null;
				}
			}
		});
	}

	public static JSONObject communicate(String urlString, String jsonString) {
		try {
			byte[] data = jsonString.getBytes();
			// translate url " " to "%20", otherwise will be an error
			urlString = urlString.replace(" ", "%20");
			// build connection
			URL url = new URL(urlString);
			HttpURLConnection connection = (HttpURLConnection) url
					.openConnection();
			connection.setDoOutput(true);
			connection.setDoInput(true);
			connection.setFixedLengthStreamingMode(data.length);

			// write data to the server
			OutputStream outputStream = connection.getOutputStream();
			outputStream.write(data);

			// read feedback
			BufferedReader reader = new BufferedReader(new InputStreamReader(
					connection.getInputStream()));
			String lines;
			StringBuffer sb = new StringBuffer("");
			while ((lines = reader.readLine()) != null) {
				lines = new String(lines.getBytes());
				sb.append(lines);
			}
			reader.close();
			// disconnect the server
			connection.disconnect();
			// pack the json and return it.
			String out = sb.toString();
			JSONObject jo;
			if (out != null){
				jo = new JSONObject(out);
			} else {
				jo = null;
			}
			return jo;
		} catch (MalformedURLException e) {
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (JSONException e) {
			e.printStackTrace();
		}
		return null;
	}
}
