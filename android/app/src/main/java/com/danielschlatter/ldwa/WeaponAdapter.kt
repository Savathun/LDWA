package com.danielschlatter.ldwa

import androidx.recyclerview.widget.RecyclerView
import com.danielschlatter.ldwa.WeaponAdapter.ListItemHolder
import android.view.ViewGroup
import android.view.LayoutInflater
import android.view.View
import android.widget.ImageView
import android.widget.TextView
import java.util.ArrayList

class WeaponAdapter(
    private val mainActivity: MainActivity,
    private val weaponList: ArrayList<Weapon>
) : RecyclerView.Adapter<ListItemHolder>() {
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ListItemHolder {
        val listItem = LayoutInflater.from(parent.context)
            .inflate(R.layout.list_item, parent, false)
        return ListItemHolder(listItem)
    }

    override fun onBindViewHolder(holder: ListItemHolder, position: Int) {
        val weapon = weaponList[position]
        holder.textViewName.text = weapon.name
        holder.icon.setImageResource(
            mainActivity.resources.getIdentifier(
                weapon.getIcon(),
                "mipmap",
                mainActivity.packageName
            )
        )
        holder.element.setImageResource(
            mainActivity.resources.getIdentifier(
                weapon.getElementIcon(),
                "mipmap",
                mainActivity.packageName
            )
        )
        holder.ammo.setImageResource(
            mainActivity.resources.getIdentifier(
                weapon.getAmmoIcon(),
                "mipmap",
                mainActivity.packageName
            )
        )
    }

    override fun getItemCount(): Int {
        return weaponList.size
    }

    inner class ListItemHolder(view: View) : RecyclerView.ViewHolder(view), View.OnClickListener {
        val textViewName: TextView = view.findViewById(R.id.textViewName)
        val icon: ImageView = view.findViewById(R.id.icon)
        val element: ImageView = view.findViewById(R.id.element)
        val ammo: ImageView = view.findViewById(R.id.ammo)
        override fun onClick(view: View) {
            mainActivity.showWeapon(adapterPosition)
        }

        init {
            view.isClickable = true
            view.setOnClickListener(this)
        }
    }
}