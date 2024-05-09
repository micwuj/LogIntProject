package com.example.loginttester2;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.Firebase;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;


public class MainActivity extends AppCompatActivity {
    Button button_confirm;
    EditText editTextDriver;
    EditText editTextPackage;
    EditText editTextAction;
    EditText editTextDateTime;
    String textDriver;
    String textPackage;
    String textAction;
    String textDateTime;

    DatabaseReference reference;
    FirebaseDatabase db;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        button_confirm = (Button) findViewById(R.id.button);
        editTextDriver = (EditText) findViewById(R.id.editTextDriver);
        editTextPackage = (EditText) findViewById(R.id.editTextPackage);
        editTextAction = (EditText) findViewById(R.id.editTextAction);
        editTextDateTime = (EditText) findViewById(R.id.editTextDateTime);


        button_confirm.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                textDriver = editTextDriver.getText().toString();
                textPackage = editTextPackage.getText().toString();
                textAction = editTextAction.getText().toString();
                textDateTime = editTextDateTime.getText().toString();

                addRecord();
//                System.out.println(textDriver);
            }
        });
    }

    public void addRecord(){
        if(textDriver.isEmpty() || textPackage.isEmpty() || textAction.isEmpty() || textDateTime.isEmpty()){
            Toast.makeText(MainActivity.this,"Provide all fields",Toast.LENGTH_SHORT);
            System.out.println("NOTsended");

        }
        else {
//            String id = databaseReference.push().getKey();
            Record newRecord = new Record(textDriver,textPackage,textAction,textDateTime);
            db = FirebaseDatabase.getInstance();
            reference = db.getReference("Records");
            reference.child(textDriver).setValue(newRecord).addOnCompleteListener(new OnCompleteListener<Void>() {
                @Override
                public void onComplete(@NonNull Task<Void> task) {
                    System.out.println("data sended");


                    editTextDriver.setText("");
                    editTextPackage.setText("");
                    editTextAction.setText("");
                    editTextDateTime.setText("");
                    Toast.makeText(MainActivity.this,"Data sent",Toast.LENGTH_SHORT).show();
                }
            });
        }
    }
}