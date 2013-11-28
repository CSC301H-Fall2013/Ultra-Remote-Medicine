package com.example.myapp;

import org.json.JSONArray;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.Toast;

public class PatientPageActivity extends ActivityAPI {
	Context mContext;
	private int currentGroup = 0;
	private TextView pPatientName;
	private TextView pPatientUrmid;
	private TextView pPatientSex;
	private TextView pPatientDob;
	private TextView pPatientHealthId;
	private TextView pPatientGps;
	private TextView pPatientAddress;
	private TextView pPatientPhone;
	private TextView pPatientEmail;

	private TextView pCaseIdA2;
	private TextView pCaseDateA3;
	private TextView pCaseSpecialtyA4;
	private TextView pCaseReviewerA5;
	private TextView pCasePriorityA6;

	private TextView pCaseIdB2;
	private TextView pCaseDateB3;
	private TextView pCaseSpecialtyB4;
	private TextView pCaseReviewerB5;
	private TextView pCasePriorityB6;

	private TextView pCaseIdC2;
	private TextView pCaseDateC3;
	private TextView pCaseSpecialtyC4;
	private TextView pCaseReviewerC5;
	private TextView pCasePriorityC6;

	private TextView pCaseIdD2;
	private TextView pCaseDateD3;
	private TextView pCaseSpecialtyD4;
	private TextView pCaseReviewerD5;
	private TextView pCasePriorityD6;

	private Button preButton;
	private Button nextButton;

	private TableRow ptableRowA1Btn;
	private TableRow ptableRowB1Btn;
	private TableRow ptableRowC1Btn;
	private TableRow ptableRowD1Btn;

	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.patient_page);
		mContext = this;
		Button newCaseButton = (Button) findViewById(R.id.patientpage_add_new_case_btn);
		preButton = (Button) findViewById(R.id.patientpage_pre_btn);
		nextButton = (Button) findViewById(R.id.patientpage_next_btn);
		pPatientName = (TextView) findViewById(R.id.patientpage_patient_name);
		pPatientUrmid = (TextView) findViewById(R.id.patientpage_patient_urmid);
		pPatientSex = (TextView) findViewById(R.id.patientpage_patient_sex);
		pPatientDob = (TextView) findViewById(R.id.patientpage_patient_dob);
		pPatientHealthId = (TextView) findViewById(R.id.patientpage_patient_health_id);
		pPatientGps = (TextView) findViewById(R.id.patientpage_patient_gps);
		pPatientAddress = (TextView) findViewById(R.id.patientpage_patient_address);
		pPatientPhone = (TextView) findViewById(R.id.patientpage_patient_phone);
		pPatientEmail = (TextView) findViewById(R.id.patientpage_patient_email);

		pCaseIdA2 = (TextView) findViewById(R.id.patientpage_case_num_A2);
		pCaseDateA3 = (TextView) findViewById(R.id.patientpage_case_date_A3);
		pCaseSpecialtyA4 = (TextView) findViewById(R.id.patientpage_case_specialty_A4);
		pCaseReviewerA5 = (TextView) findViewById(R.id.patientpage_case_reviewer_A5);
		pCasePriorityA6 = (TextView) findViewById(R.id.patientpage_case_priority_A6);

		pCaseIdB2 = (TextView) findViewById(R.id.patientpage_case_num_B2);
		pCaseDateB3 = (TextView) findViewById(R.id.patientpage_case_date_B3);
		pCaseSpecialtyB4 = (TextView) findViewById(R.id.patientpage_case_specialty_B4);
		pCaseReviewerB5 = (TextView) findViewById(R.id.patientpage_case_reviewer_B5);
		pCasePriorityB6 = (TextView) findViewById(R.id.patientpage_case_priority_B6);

		pCaseIdC2 = (TextView) findViewById(R.id.patientpage_case_num_C2);
		pCaseDateC3 = (TextView) findViewById(R.id.patientpage_case_date_C3);
		pCaseSpecialtyC4 = (TextView) findViewById(R.id.patientpage_case_specialty_C4);
		pCaseReviewerC5 = (TextView) findViewById(R.id.patientpage_case_reviewer_C5);
		pCasePriorityC6 = (TextView) findViewById(R.id.patientpage_case_priority_C6);

		pCaseIdD2 = (TextView) findViewById(R.id.patientpage_case_num_D2);
		pCaseDateD3 = (TextView) findViewById(R.id.patientpage_case_date_D3);
		pCaseSpecialtyD4 = (TextView) findViewById(R.id.patientpage_case_specialty_D4);
		pCaseReviewerD5 = (TextView) findViewById(R.id.patientpage_case_reviewer_D5);
		pCasePriorityD6 = (TextView) findViewById(R.id.patientpage_case_priority_D6);

		ptableRowA1Btn = (TableRow) findViewById(R.id.patientpage_tableRowA1);
		ptableRowB1Btn = (TableRow) findViewById(R.id.patientpage_tableRowB1);
		ptableRowC1Btn = (TableRow) findViewById(R.id.patientpage_tableRowC1);
		ptableRowD1Btn = (TableRow) findViewById(R.id.patientpage_tableRowD1);

		loadPatientInfo();
		loadCases();

		// Button Click event for "new case" button
		newCaseButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				// navigate to add new case page
				jsonCurCaseId = null;
				jsonCurCase = null;
				Intent i = new Intent(mContext, AddNewCaseActivity.class);
				startActivity(i);
			}
		});

		// Button Click event for "pre" button
		preButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				// navigate to add new case page
				currentGroup--;
				displayCases();
			}
		});

		// Button Click event for "next" button
		nextButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				// navigate to add new case page
				currentGroup++;
				displayCases();
			}
		});

		// Button Click event for "RowA" button
		ptableRowA1Btn.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				jsonCurCaseId = null;
				JSONArray list = jsonCurCaseList.optJSONArray("cases");
				jsonCurCase = list.optJSONObject(currentGroup * 4);
				Intent i = new Intent(mContext, CasePageActivity.class);
				startActivity(i);
			}
		});

		// Button Click event for "RowB" button
		ptableRowB1Btn.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				jsonCurCaseId = null;
				JSONArray list = jsonCurCaseList.optJSONArray("cases");
				jsonCurCase = list.optJSONObject(currentGroup * 4 + 1);
				Intent i = new Intent(mContext, CasePageActivity.class);
				startActivity(i);
			}
		});

		// Button Click event for "RowC" button
		ptableRowC1Btn.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				jsonCurCaseId = null;
				JSONArray list = jsonCurCaseList.optJSONArray("cases");
				jsonCurCase = list.optJSONObject(currentGroup * 4 + 2);
				Intent i = new Intent(mContext, CasePageActivity.class);
				startActivity(i);
			}
		});

		// Button Click event for "RowD" button
		ptableRowD1Btn.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				jsonCurCaseId = null;
				JSONArray list = jsonCurCaseList.optJSONArray("cases");
				jsonCurCase = list.optJSONObject(currentGroup * 4 + 3);
				Intent i = new Intent(mContext, CasePageActivity.class);
				startActivity(i);
			}
		});
	}

	/* Helper function to load current patient information */
	private void loadPatientInfo() {

		pPatientName.setText("Patient: ");
		pPatientUrmid.setText("U.R.M ID: ");
		pPatientSex.setText("Sex: ");
		pPatientDob.setText("DOB: ");
		pPatientHealthId.setText("Health ID: ");
		pPatientGps.setText("GPS: ");
		pPatientAddress.setText("Addr: ");
		pPatientPhone.setText("Tel: ");
		pPatientEmail.setText("Email: ");

		if (jsonCurPatient == null) {
			if (jsonCurPatientId != null) {
				// Create a new thread to load patient data
				Thread thread = new Thread(new Runnable() {
					@Override
					public void run() {
						try {
							// URL
							String urlString = "view_patient";
							// Json package string
							String jsonString = "{\"session_key\": \""
									+ jsonCurSessionId.getString("sessionid")
									+ "\", \"patient_id\": \""
									+ jsonCurPatientId.getString("patient_id")
									+ "\"}";

							jsonCurPatient = communicate(urlString, jsonString);

						} catch (Exception e) {
							e.printStackTrace();
						}
					}
				});
				thread.start();

				// wait for the server respond
				int timer = 0;
				while (jsonCurPatient == null && timer < 50) {
					try {
						Thread.sleep(200);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
					timer++;
				}
				Toast msg = Toast.makeText(getBaseContext(),
						(timer < 50 ? jsonCurPatient.optString("firstName")
								: "Server time out"), Toast.LENGTH_LONG);
				msg.show();
				msg = null;
				if (jsonCurPatient == null
						|| jsonCurPatient.optString("success").equals("false")) {
					// If server can not find the key, then navigate to dash
					// board
					jsonCurPatient = null;

					Intent i = new Intent(mContext, DashboardActivity.class);
					startActivity(i);
				}
			} else {
				Intent i = new Intent(mContext, DashboardActivity.class);
				startActivity(i);
			}
		}
		pPatientName.setText("Patient: " + jsonCurPatient.optString("lastName")
				+ ", " + jsonCurPatient.optString("firstName"));
		pPatientUrmid.setText("U.R.M ID: "
				+ jsonCurPatient.optString("patient_id"));
		pPatientSex.setText("Sex: " + jsonCurPatient.optString("gender"));
		pPatientDob
				.setText("DOB: " + jsonCurPatient.optString("date_of_birth"));
		pPatientHealthId.setText("Health ID: "
				+ jsonCurPatient.optString("health_id"));
		pPatientGps.setText("GPS: "
				+ jsonCurPatient.optString("gps_coordinates"));
		pPatientAddress.setText("Addr: " + jsonCurPatient.optString("address"));
		pPatientPhone.setText("Tel: " + jsonCurPatient.optString("phone"));
		pPatientEmail.setText("Email: " + jsonCurPatient.optString("email"));
	}

	/* Helper function to load current patient's cases */
	private void loadCases() {
		if (jsonCurCaseList == null) {
			if (jsonCurPatient != null) {
				// Create a new thread to load patient data
				Thread thread = new Thread(new Runnable() {
					@Override
					public void run() {
						try {
							// URL
							String urlString = "display_patient_cases";
							// Json package string
							String jsonString = "{\"session_key\": \""
									+ jsonCurSessionId.getString("sessionid")
									+ "\", \"patient_id\": \""
									+ AddNewPatientActivity.jsonCurPatient
											.getString("patient_id") + "\"}";

							jsonCurCaseList = communicate(urlString, jsonString);

						} catch (Exception e) {
							e.printStackTrace();
						}
					}
				});
				thread.start();

				// wait for the server respond
				int timer = 0;
				while (jsonCurCaseList == null && timer < 50) {
					try {
						Thread.sleep(200);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
					timer++;
				}
				Toast msg = Toast.makeText(getBaseContext(),
						(timer < 50 ? jsonCurCaseList.optString("type")
								: "Server time out"), Toast.LENGTH_LONG);
				msg.show();
				msg = null;
				if (jsonCurCaseList == null
						|| jsonCurCaseList.optString("success").equals("false")) {
					// If server can not find the key, then navigate to dash
					// board
					jsonCurCaseList = null;
				} else {
					currentGroup = 0;
					displayCases();
				}
			}
		}else if (jsonCurPatient != null){
			currentGroup = 0;
			displayCases();
		}
	}

	/* Helper function to display patient's cases */
	private void displayCases() {
		pCaseIdA2.setText("");
		pCaseDateA3.setText("");
		pCaseSpecialtyA4.setText("");
		pCaseReviewerA5.setText("");
		pCasePriorityA6.setText("");

		pCaseIdB2.setText("");
		pCaseDateB3.setText("");
		pCaseSpecialtyB4.setText("");
		pCaseReviewerB5.setText("");
		pCasePriorityB6.setText("");

		pCaseIdC2.setText("");
		pCaseDateC3.setText("");
		pCaseSpecialtyC4.setText("");
		pCaseReviewerC5.setText("");
		pCasePriorityC6.setText("");

		pCaseIdD2.setText("");
		pCaseDateD3.setText("");
		pCaseSpecialtyD4.setText("");
		pCaseReviewerD5.setText("");
		pCasePriorityD6.setText("");

		ptableRowA1Btn.setEnabled(false);
		ptableRowB1Btn.setEnabled(false);
		ptableRowC1Btn.setEnabled(false);
		ptableRowD1Btn.setEnabled(false);
		preButton.setEnabled(false);
		nextButton.setEnabled(false);

		if (jsonCurCaseList != null) {
			JSONArray list = jsonCurCaseList.optJSONArray("cases");
			if (list.length() > 0) {
				int maxGroup = list.length() / 4;
				if (list.length() % 4 == 0){
					maxGroup--;
				}

				if (currentGroup <= 0) {
					// disable pre btn
					preButton.setEnabled(false);
				} else {
					// enable pre btn
					preButton.setEnabled(true);
				}
				if (currentGroup >= maxGroup) {
					// disable next btn
					nextButton.setEnabled(false);
				} else {
					// enable next btn
					nextButton.setEnabled(true);
				}

				// display case on first block
				pCaseIdA2.setText("Case#: "
						+ list.optJSONObject(currentGroup * 4).optString(
								"case_id"));
				pCaseDateA3.setText("Date: "
						+ list.optJSONObject(currentGroup * 4).optString(
								"creation_date"));
				pCaseSpecialtyA4.setText("Spe: "
						+ list.optJSONObject(currentGroup * 4).optString(
								"specialty"));
				pCaseReviewerA5.setText("Submitter: "
						+ list.optJSONObject(currentGroup * 4).optString(
								"submitter"));
				pCasePriorityA6.setText("Priority: "
						+ list.optJSONObject(currentGroup * 4).optString(
								"priority"));

				ptableRowA1Btn.setEnabled(true);

				// display case on second block
				if (currentGroup != maxGroup || list.length() % 4 == 0
						|| list.length() % 4 > 1) {
					pCaseIdB2.setText("Case#: "
							+ list.optJSONObject(currentGroup * 4 + 1)
									.optString("case_id"));
					pCaseDateB3.setText("Date: "
							+ list.optJSONObject(currentGroup * 4 + 1)
									.optString("creation_date"));
					pCaseSpecialtyB4.setText("Spe: "
							+ list.optJSONObject(currentGroup * 4 + 1)
									.optString("specialty"));
					pCaseReviewerB5.setText("Submitter: "
							+ list.optJSONObject(currentGroup * 4 + 1).optString(
									"submitter"));
					pCasePriorityB6.setText("Priority: "
							+ list.optJSONObject(currentGroup * 4 + 1)
									.optString("priority"));

					ptableRowB1Btn.setEnabled(true);
				}

				// display case on third block
				if (currentGroup != maxGroup || list.length() % 4 == 0
						|| list.length() % 4 > 2) {
					pCaseIdC2.setText("Case#: "
							+ list.optJSONObject(currentGroup * 4 + 2)
									.optString("case_id"));
					pCaseDateC3.setText("Date: "
							+ list.optJSONObject(currentGroup * 4 + 2)
									.optString("creation_date"));
					pCaseSpecialtyC4.setText("Spe: "
							+ list.optJSONObject(currentGroup * 4 + 2)
									.optString("specialty"));
					pCaseReviewerC5.setText("Submitter: "
							+ list.optJSONObject(currentGroup * 4 + 2).optString(
									"submitter"));
					pCasePriorityC6.setText("Priority: "
							+ list.optJSONObject(currentGroup * 4 + 2)
									.optString("priority"));
					ptableRowC1Btn.setEnabled(true);
				}

				// display case on fourth block
				if (currentGroup != maxGroup || list.length() % 4 == 0) {
					pCaseIdD2.setText("Case#: "
							+ list.optJSONObject(currentGroup * 4 + 3)
									.optString("case_id"));
					pCaseDateD3.setText("Date: "
							+ list.optJSONObject(currentGroup * 4 + 3)
									.optString("creation_date"));
					pCaseSpecialtyD4.setText("Spe: "
							+ list.optJSONObject(currentGroup * 4 + 3)
									.optString("specialty"));
					pCaseReviewerD5.setText("Submitter: "
							+ list.optJSONObject(currentGroup * 4 + 3).optString(
									"submitter"));
					pCasePriorityD6.setText("Priority: "
							+ list.optJSONObject(currentGroup * 4 + 3)
									.optString("priority"));
					ptableRowD1Btn.setEnabled(true);
				}

			}
		}
	}

}