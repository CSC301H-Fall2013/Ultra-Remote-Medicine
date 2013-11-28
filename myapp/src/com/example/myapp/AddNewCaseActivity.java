package com.example.myapp;

import java.io.ByteArrayOutputStream;

import org.json.JSONObject;

import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.Toast;

public class AddNewCaseActivity extends ActivityAPI {
	Context mContext;
	private EditText mPatientID;
	private Spinner mPatientPriority;
	private String mPatientPriorityInt;
	private EditText mPatientComments;
	private ImageView mImage;
	private static JSONObject jsonCheck;
	private static String photo;
	private static int RESULT_LOAD_IMAGE = 1;

	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.add_new_case);
		mContext = this;
		mPatientID = (EditText) findViewById(R.id.patient_id);
		mPatientPriority = (Spinner) findViewById(R.id.patient_priority);
		mPatientComments = (EditText) findViewById(R.id.patient_comments);
		mImage = (ImageView) findViewById(R.id.add_new_case_pic);

		if (jsonCurPatientId != null){
			mPatientID.setText(jsonCurPatientId.optString("patient_id"));
		}
			
		// Click event for the adding a picture for phone's picture gallery
		Button picButton = (Button) findViewById(R.id.add_new_case_add);
		picButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				Intent i = new Intent(
						Intent.ACTION_PICK,
						android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
				startActivityForResult(i, RESULT_LOAD_IMAGE);
			}
		});

		// Click event for sending the data to the server
		Button finishButton = (Button) findViewById(R.id.add_case_finish);
		finishButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				jsonCurCaseId = null;

				// read the case priority.
				mPatientPriorityInt = mPatientPriority.getSelectedItem()
						.toString();
				if (mPatientPriorityInt.equals("Low")) {
					mPatientPriorityInt = "30";
				} else if (mPatientPriorityInt.equals("Medium")) {
					mPatientPriorityInt = "20";
				} else {
					// High priority
					mPatientPriorityInt = "10";
				}

				// create a new thread to upload data
				Thread thread = new Thread(new Runnable() {
					@Override
					public void run() {
						try {
							// URL
							String urlString = "add_case";
							// Json package
							String jsonString = "{\"session_key\": \""
									+ jsonCurSessionId.optString("sessionid")
									+ "\", \"patient\": \""
									+ mPatientID.getText().toString()
									+ "\", \"comments\": \""
									+ mPatientComments.getText().toString()
									+ "\", \"priority\": \""
									+ mPatientPriorityInt + "\"}";

							jsonCurCaseId = communicate(urlString, jsonString);

						} catch (Exception e) {
							e.printStackTrace();
						}
					}
				});
				thread.start();

				// wait for the server respond
				int timer = 0;
				while (jsonCurCaseId == null && timer < 50) {
					try {
						Thread.sleep(200);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
					timer++;
				}
				if (jsonCurCaseId != null
						&& jsonCurCaseId.optString("success").equals("true")) {
					// if the case was successfully created, then upload the
					// picture
					upLoadPic();
				} else {
					Toast msg = Toast.makeText(getBaseContext(),
							(timer < 50 ? jsonCurCaseId.optString("type")
									: "Server time out"), Toast.LENGTH_LONG);
					msg.show();
					msg = null;
					jsonCurCaseId = null;
				}
			}
		});
	}

	/* Helper function for upload the selective picture */
	private void upLoadPic() {

		// convert the picture to 64 bit String
		Bitmap bm = ((BitmapDrawable) mImage.getDrawable()).getBitmap();
		ByteArrayOutputStream baos = new ByteArrayOutputStream();
		bm.compress(Bitmap.CompressFormat.JPEG, 100, baos);
		byte[] b = baos.toByteArray();
		photo = Base64.encodeToString(b, Base64.DEFAULT);

		jsonCheck = null;

		// create a new thread to upload picture
		Thread threadpic = new Thread(new Runnable() {
			@Override
			public void run() {
				try {
					// URL
					String urlString = "upload";
					// Json package
					String jsonString = "{\"session_key\": \""
							+ jsonCurSessionId.optString("sessionid")
							+ "\", \"case_id\": \""
							+ jsonCurCaseId.optString("case_id")
							+ "\", \"image_string\": \"" + photo + "\"}";

					jsonCheck = communicate(urlString, jsonString);

				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
		threadpic.start();

		// wait for the server respond
		int timer = 0;
		while (jsonCheck == null && timer < 300) {
			try {
				Thread.sleep(200);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			timer++;
		}

		if (jsonCheck != null && jsonCheck.optString("success").equals("true")) {
			// if server created the case, then navigate to Case Page
			Intent i = new Intent(mContext, CasePageActivity.class);
			startActivity(i);
		} else {
			Toast msg = Toast.makeText(getBaseContext(),
					(timer < 50 ? jsonCheck.optString("success")
							: "Server time out"), Toast.LENGTH_LONG);
			msg.show();
			msg = null;
			jsonCheck = null;
		}
	}

	/* Select a picture from phone's gallery */
	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		super.onActivityResult(requestCode, resultCode, data);

		if (requestCode == RESULT_LOAD_IMAGE && resultCode == RESULT_OK
				&& null != data) {
			Uri selectedImage = data.getData();
			String[] filePathColumn = { MediaStore.Images.Media.DATA };

			Cursor cursor = getContentResolver().query(selectedImage,
					filePathColumn, null, null, null);
			cursor.moveToFirst();

			int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
			String picturePath = cursor.getString(columnIndex);
			cursor.close();

			// set the imageView box to the selective picture from Gallery
			mImage.setImageBitmap(BitmapFactory.decodeFile(picturePath));

		}

	}

}
