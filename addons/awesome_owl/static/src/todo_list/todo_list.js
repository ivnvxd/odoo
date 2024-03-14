/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.todoIdCounter = 0;
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value !== "") {
            this.todos.push({
                id: this.todoIdCounter++,
                description: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }
}
