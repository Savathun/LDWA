package com.danielschlatter.ldwa

import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.os.StrictMode
import android.os.StrictMode.ThreadPolicy
import android.util.Log
import android.view.Menu
import android.view.MenuItem
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.Toolbar
import androidx.recyclerview.widget.DividerItemDecoration
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import java.io.BufferedReader
import java.io.IOException
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.MalformedURLException
import java.net.URL

class MainActivity : AppCompatActivity() {
    private var weaponList: ArrayList<Weapon>? = null
    private var dataAdapter: DataAdapter? = null
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val policy = ThreadPolicy.Builder().permitAll().build()
        StrictMode.setThreadPolicy(policy)
        val toolbar = findViewById<Toolbar>(R.id.toolbar)
        toolbar.setTitleTextColor(Color.WHITE)
        setSupportActionBar(toolbar)
        var obj: URL? = null
        try {
            obj =
                URL("https://raw.githubusercontent.com/Savathun/LDWA/main/python/manifest/manifest_version.txt")
        } catch (e: MalformedURLException) {
            e.printStackTrace()
        }
        try {
            assert(obj != null)
            val con = obj!!.openConnection() as HttpURLConnection
            con.requestMethod = "GET"
            val `in` = BufferedReader(InputStreamReader(con.inputStream))
            if (getString(R.string.manifest_version) != `in`.readLine()) {
                Log.e("update", "update needed")
            }
        } catch (e: IOException) {
            e.printStackTrace()
        }
        weaponList = ArrayList()
        dataAdapter = DataAdapter(this)
        dataAdapter!!.createDatabase()
        dataAdapter!!.open()
        val recyclerView = findViewById<RecyclerView>(R.id.recyclerView)
        val weaponAdapter = WeaponAdapter(this, weaponList!!)
        val layoutManager: RecyclerView.LayoutManager = LinearLayoutManager(applicationContext)
        recyclerView.layoutManager = layoutManager
        recyclerView.addItemDecoration(DividerItemDecoration(this, LinearLayoutManager.VERTICAL))
        recyclerView.adapter = weaponAdapter
    }

    override fun onResume() {
        super.onResume()
        loadData()
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        // Inflate the menu; this adds items to the action bar if it is present.
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        val id = item.itemId
        if (id == R.id.action_settings) {
            startActivity(Intent(this, SettingsActivity::class.java))
            return true
        }
        return super.onOptionsItemSelected(item)
    }

    fun showWeapon(weaponToShow: Int) {
        val viewWeaponDialog = dataAdapter?.let { ViewWeaponDialog(it) }
        viewWeaponDialog?.sendSelectedWeapon(weaponList!![weaponToShow])
        viewWeaponDialog?.show(supportFragmentManager, "")
    }

    private fun loadData() {
        val cursor = dataAdapter!!.selectAll()
        val weaponCount = cursor.count
        if (weaponCount != weaponList!!.size) {
            weaponList!!.clear()
            while (cursor.moveToNext()) {
                val id = cursor.getInt(cursor.getColumnIndex("index"))
                val name = cursor.getString(cursor.getColumnIndex("Name"))
                val type = cursor.getString(cursor.getColumnIndex("Type"))
                val archetype = cursor.getString(cursor.getColumnIndex("Archetype"))
                val icon = cursor.getString(cursor.getColumnIndex("Icon"))
                val element = cursor.getString(cursor.getColumnIndex("Element"))
                val slot = cursor.getString(cursor.getColumnIndex("Slot"))
                val ammo = cursor.getString(cursor.getColumnIndex("Ammo"))
                val ammoIcon = cursor.getString(cursor.getColumnIndex("AmmoIcon"))
                val synergy = cursor.getString(cursor.getColumnIndex("Synergy"))
                val perkColumn1 = cursor.getString(cursor.getColumnIndex("perk_column_1"))
                val perkColumn2 = cursor.getString(cursor.getColumnIndex("perk_column_2"))
                val perkColumn3 = cursor.getString(cursor.getColumnIndex("perk_column_3"))
                val perkColumn4 = cursor.getString(cursor.getColumnIndex("perk_column_4"))
                val screenshot = cursor.getString(cursor.getColumnIndex("Screenshot"))
                val elementIcon = cursor.getString(cursor.getColumnIndex("ElementIcon"))
                val weapon = Weapon(
                    id,
                    name,
                    type,
                    archetype,
                    icon,
                    ammoIcon,
                    synergy,
                    perkColumn1,
                    perkColumn2,
                    perkColumn3,
                    perkColumn4,
                    screenshot,
                    elementIcon
                )
                weaponList!!.add(weapon)
            }
        }
    }
}