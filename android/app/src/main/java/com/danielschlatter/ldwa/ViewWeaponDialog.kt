package com.danielschlatter.ldwa

import android.app.AlertDialog
import android.app.Dialog
import android.os.Bundle
import android.view.Gravity
import android.widget.*
import androidx.fragment.app.DialogFragment

class ViewWeaponDialog(private val dataAdapter: DataAdapter) : DialogFragment() {
    private var weapon: Weapon? = null
    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        val dialog = super.onCreateDialog(savedInstanceState)
        dialog.setCanceledOnTouchOutside(true)
        val inflater = requireActivity().layoutInflater
        val title = inflater.inflate(R.layout.title_bar, null)
        val name = title.findViewById<TextView>(R.id.name)
        name.text = weapon!!.name
        val type = title.findViewById<TextView>(R.id.type)
        val archetype = title.findViewById<TextView>(R.id.archetype)
        val icon = title.findViewById<ImageView>(R.id.icon)
        val ammoIcon = title.findViewById<ImageView>(R.id.ammo)
        val elementIcon = title.findViewById<ImageView>(R.id.element)
        type.text = weapon!!.type
        archetype.text = weapon!!.archetype
        icon.setImageResource(
            requireContext().resources.getIdentifier(
                weapon!!.getIcon(),
                "mipmap",
                requireContext().packageName
            )
        )
        elementIcon.setImageResource(
            requireContext().resources.getIdentifier(
                weapon!!.getElementIcon(),
                "mipmap",
                requireContext().packageName
            )
        )
        ammoIcon.setImageResource(
            requireContext().resources.getIdentifier(
                weapon!!.getAmmoIcon(),
                "mipmap",
                requireContext().packageName
            )
        )
        val builder = AlertDialog.Builder(activity).setCustomTitle(title)
        val dialogView = inflater.inflate(R.layout.dialog_view_weapon, null)
        val screenshot = dialogView.findViewById<ImageView>(R.id.imageViewScreenshot)
        val synergyTextView = dialogView.findViewById<TextView>(R.id.textViewSynergy)
        val buttonClose = dialogView.findViewById<Button>(R.id.buttonClose)
        if (weapon!!.synergy == "set()") synergyTextView.setText(R.string.no_synergy) else synergyTextView.text =
            weapon!!.synergy
        screenshot.setImageResource(
            requireContext().resources.getIdentifier(
                weapon!!.getScreenshot(),
                "drawable",
                requireContext().packageName
            )
        )
        if (weapon!!.perk_column_1 != "'Static'") {
            val perkColumn1 = weapon!!.perk_column_1.split(", ").toTypedArray()
            val perkColumn2 = weapon!!.perk_column_2.split(", ").toTypedArray()
            val perkColumn3 = weapon!!.perk_column_3.split(", ").toTypedArray()
            val perkColumn4 = weapon!!.perk_column_4.split(", ").toTypedArray()
            val perks = arrayOf(perkColumn1, perkColumn2, perkColumn3, perkColumn4)
            val rg = arrayOf(
                dialogView.findViewById(R.id.rg1),
                dialogView.findViewById(R.id.rg2),
                dialogView.findViewById(R.id.rg3),
                dialogView.findViewById<RadioGroup>(R.id.rg4)
            )
            for (i in perks.indices) {
                for (j in 0 until perks[i].size) {
                    val temp = RadioButton(requireContext())
                    temp.contentDescription = perks[i][j]
                    val id = requireContext().resources.getIdentifier(
                        dataAdapter.selectPerk(perks[i][j].substring(1, perks[i][j].length - 1)),
                        "mipmap",
                        requireContext().packageName
                    )
                    temp.foreground = resources.getDrawable(id)
                    temp.setBackgroundResource(R.drawable.perk_background)
                    temp.gravity = Gravity.CENTER
                    temp.tag = id
                    val params = RadioGroup.LayoutParams(130, 130)
                    params.setMargins(0, 5, 0, 5)
                    temp.layoutParams = params
                    temp.setButtonDrawable(R.drawable.transparent)
                    rg[i].addView(temp)
                    if (j == 0) rg[i].check(temp.id)
                }
            }
            val cursor = dataAdapter.selectRolls(weapon!!.name)
            val ll = dialogView.findViewById<LinearLayout>(R.id.table)
            while (cursor.moveToNext()) {
                val row = LinearLayout(requireContext())
                for (i in 1..4) {
                    val iv = ImageView(requireContext())
                    iv.setImageResource(cursor.getInt(i))
                    iv.layoutParams = LinearLayout.LayoutParams(130, 130, 1F)
                    row.addView(iv)
                }
                val button = Button(requireContext())
                button.setBackgroundResource(R.drawable.x)
                button.setOnClickListener {
                    val tempCursor = dataAdapter.selectRolls(
                        weapon!!.name
                    )
                    tempCursor.moveToPosition((row.tag as Int))
                    ll.removeView(row)
                    dataAdapter.removeRoll(
                        weapon!!.name,
                        tempCursor.getInt(1),
                        tempCursor.getInt(2),
                        tempCursor.getInt(3),
                        tempCursor.getInt(4)
                    )
                    tempCursor.close()
                }
                val parameters = LinearLayout.LayoutParams(10, 70, 0.6f)
                parameters.setMargins(0, 0, 10, 0)
                button.layoutParams = parameters
                button.gravity = Gravity.CENTER_VERTICAL
                row.addView(button)
                row.gravity = Gravity.CENTER_VERTICAL
                row.tag = cursor.position
                ll.addView(row)
            }
            cursor.close()
            val buttonSave = dialogView.findViewById<Button>(R.id.save_button)
            buttonSave.setOnClickListener {
                val row = LinearLayout(requireContext())
                val ids = IntArray(4)
                for (i in rg.indices) {
                    val temp = dialogView.findViewById<RadioButton>(rg[i].checkedRadioButtonId)
                    val iv = ImageView(requireContext())
                    ids[i] = temp.tag as Int
                    iv.setImageResource(ids[i])
                    iv.layoutParams = LinearLayout.LayoutParams(130, 130, 1F)
                    row.addView(iv)
                }
                val button = Button(requireContext())
                button.setBackgroundResource(R.drawable.x)
                button.setOnClickListener {
                    val tempCursor = dataAdapter.selectRolls(
                        weapon!!.name
                    )
                    tempCursor.moveToPosition((row.tag as Int))
                    ll.removeView(row)
                    dataAdapter.removeRoll(weapon!!.name, ids[0], ids[1], ids[2], ids[3])
                }
                val parameters = LinearLayout.LayoutParams(10, 70, 0.6f)
                parameters.setMargins(0, 0, 10, 0)
                button.layoutParams = parameters
                button.gravity = Gravity.CENTER_VERTICAL
                row.addView(button)
                row.gravity = Gravity.CENTER_VERTICAL
                val tempCursor = dataAdapter.selectRolls(weapon!!.name)
                row.tag = tempCursor.count
                tempCursor.close()
                ll.addView(row)
                dataAdapter.insertRoll(weapon!!.name, ids[0], ids[1], ids[2], ids[3])
            }
        }
        builder.setView(dialogView).setMessage(" ")
        buttonClose.setOnClickListener { dismiss() }
        return builder.create()
    }

    fun sendSelectedWeapon(weapon: Weapon?) {
        this.weapon = weapon
    }
}