package com.danielschlatter.ldwa;

import android.content.Intent;
import android.database.Cursor;
import android.graphics.Color;
import android.os.Bundle;
import android.os.StrictMode;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {
    private ArrayList<Weapon> weaponList;
    private DataAdapter dataAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        Toolbar toolbar = findViewById(R.id.toolbar);
        toolbar.setTitleTextColor(Color.WHITE);
        setSupportActionBar(toolbar);
        URL obj = null;
        try {
            obj = new URL("https://raw.githubusercontent.com/Savathun/LDWA/main/python/manifest/manifest_version.txt");
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }
        try {
            assert obj != null;
            HttpURLConnection con = (HttpURLConnection) obj.openConnection();
            con.setRequestMethod("GET");
            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));

            if(!getString(R.string.manifest_version).equals(in.readLine())){
                Log.e("update", "update needed");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }


        weaponList = new ArrayList<>();
        dataAdapter = new DataAdapter(this);
        dataAdapter.createDatabase();
        dataAdapter.open();
        dataAdapter.dso();
        RecyclerView recyclerView = findViewById(R.id.recyclerView);
        WeaponAdapter weaponAdapter = new WeaponAdapter(this, weaponList);

        RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(getApplicationContext());
        recyclerView.setLayoutManager(layoutManager);
        recyclerView.addItemDecoration(new DividerItemDecoration(this, LinearLayoutManager.VERTICAL));

        recyclerView.setAdapter(weaponAdapter);
    }

    @Override
    protected void onResume() {
        super.onResume();
        loadData();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            startActivity(new Intent(this, SettingsActivity.class));
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void showWeapon (int weaponToShow) {
        ViewWeaponDialog viewWeaponDialog = new ViewWeaponDialog(dataAdapter);
        viewWeaponDialog.sendSelectedWeapon(weaponList.get(weaponToShow));
        viewWeaponDialog.show(getSupportFragmentManager(), "");
    }

    public void loadData () {
        Cursor cursor = dataAdapter.selectAll();
        int weaponCount = cursor.getCount();

        if (weaponCount != weaponList.size()) {
            weaponList.clear();
            while (cursor.moveToNext()) {
                int id = cursor.getInt(cursor.getColumnIndex("index"));
                String name = cursor.getString(cursor.getColumnIndex("Name"));
                String type = cursor.getString(cursor.getColumnIndex("Type"));
                String archetype = cursor.getString(cursor.getColumnIndex("Archetype"));
                String icon = cursor.getString(cursor.getColumnIndex("Icon"));
                String element = cursor.getString(cursor.getColumnIndex("Element"));
                String slot = cursor.getString(cursor.getColumnIndex("Slot"));
                String ammo = cursor.getString(cursor.getColumnIndex("Ammo"));
                String ammo_icon = cursor.getString(cursor.getColumnIndex("AmmoIcon"));
                String synergy = cursor.getString(cursor.getColumnIndex("Synergy"));
                String perk_column_1 = cursor.getString(cursor.getColumnIndex("perk_column_1"));
                String perk_column_2 = cursor.getString(cursor.getColumnIndex("perk_column_2"));
                String perk_column_3 = cursor.getString(cursor.getColumnIndex("perk_column_3"));
                String perk_column_4 = cursor.getString(cursor.getColumnIndex("perk_column_4"));
                String screenshot = cursor.getString(cursor.getColumnIndex("Screenshot"));
                String element_icon = cursor.getString(cursor.getColumnIndex("ElementIcon"));

                Weapon weapon = new Weapon(id, name, type, archetype, icon, element, slot, ammo, ammo_icon,
                        synergy, perk_column_1, perk_column_2, perk_column_3, perk_column_4, screenshot, element_icon);

                weaponList.add(weapon);
            }
        }



    }
}