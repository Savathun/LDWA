package com.example.ldwa;

import android.database.Cursor;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {
    private ArrayList<Weapon> weaponList;
    private RecyclerView recyclerView;
    private WeaponAdapter weaponAdapter;
    private DataAdapter dataAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        weaponList = new ArrayList<Weapon>();
        dataAdapter = new DataAdapter(this);
        dataAdapter.createDatabase();
        dataAdapter.open();
        recyclerView = findViewById(R.id.recyclerView);
        weaponAdapter = new WeaponAdapter(this, weaponList);

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
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void showWeapon (int weaponToShow) {
        ViewWeaponDialog viewWeaponDialog = new ViewWeaponDialog();
        viewWeaponDialog.sendSelectedWeapon(weaponList.get(weaponToShow));
        viewWeaponDialog.show(getSupportFragmentManager(), "");
    }

    public void loadData () {
        Cursor cursor = dataAdapter.selectAll();
        int weaponCount = cursor.getCount();

        if (weaponCount > 0) {
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
        weaponAdapter.notifyDataSetChanged();


    }
}