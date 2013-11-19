package org.nepalus;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import org.json.JSONObject;
import org.json.JSONException;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class LoginScreen extends Activity {
	Context mContext;
	private EditText mPatientUserName;
	private EditText mPatientPassword;
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);
        mContext = this;
        
        Button nextButton = (Button) findViewById(R.id.login_submit);
        nextButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                mPatientUserName = (EditText) findViewById(R.id.login_username);
                mPatientPassword = (EditText) findViewById(R.id.login_password);
            	if (login(mPatientUserName.getText().toString(), 
            			mPatientPassword.getText().toString())){
            		Intent i = new Intent(mContext, MetadataScreen.class);
            		startActivity(i);
            	}
            }
        });
    }
    
	public static boolean login(String name, String password) {

		// add parameters to the URL
		String params = "?username=" + name + "&password=" + password
				+ "&format=json";
		String url = "http://localhost:8000/mobile/login" + params;

		// expect return:{"status": "ok", "response": {"data": {"password": "****", "username": "username"}}}
		JSONObject all = requestJson(url);
		//Analyse the returned json
		//JSONObject response = all.optJSONObject("response");
		//JSONObject data = response.optJSONObject("data");

		if (all.optString("status").equals("ok")) {
			return true;
		}
		return false;
	}

	/**
	 * send request to the server and pack the feedback to json
	 * 
	 * @param urlString
	 * @return
	 */
	private static JSONObject requestJson(String urlString) {
		try {
			// translate url " " to "%20", otherwise will be an error
			urlString = urlString.replace(" ", "%20");
			// build connection
			URL url = new URL(urlString);
			HttpURLConnection connection = (HttpURLConnection) url
					.openConnection();
			connection.setDoOutput(true);
			connection.setDoInput(true);
			connection.setRequestMethod("GET");
			connection.connect();

			// read feedback
			BufferedReader reader = new BufferedReader(new InputStreamReader(
					connection.getInputStream()));
			String lines;
			StringBuffer sb = new StringBuffer("");
			while ((lines = reader.readLine()) != null) {
				lines = new String(lines.getBytes(), "utf-8");
				sb.append(lines);
			}
			reader.close();
			// disconnect the server
			connection.disconnect();
            // pack the json and return it.
			JSONObject jo = new JSONObject(sb.toString());
			return jo ;
		} catch (MalformedURLException e) {
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}catch (JSONException e){
			throw new RuntimeException(e);
		}
		return null;
	}
}