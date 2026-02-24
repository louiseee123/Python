# Fix dashboard.html to add task claim buttons

with open('pokemon/templates/pokemon/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''        <div class="section">
            <h2>📋 Daily Tasks</h2>
            <div class="tasks-list">
                {% for task in daily_tasks %}
                <div class="task-item {% if task.id in completed_tasks %}task-completed{% endif %}">
                    <div class="task-info">
                        <h4>{{ task.name }}</h4>
                        <p>{{ task.description }}</p>
                    </div>
                    <div class="task-xp">+{{ task.xp_reward }} XP</div>
                </div>
                {% endfor %}
            </div>
        </div>'''

new = '''        <div class="section">
            <h2>📋 Daily Tasks</h2>
            <div class="tasks-list">
                {% for task in daily_tasks %}
                <div class="task-item {% if task.id in completed_tasks %}task-completed{% endif %}">
                    <div class="task-info">
                        <h4>{{ task.name }}</h4>
                        <p>{{ task.description }}</p>
                        {% if task.egg_reward > 0 %}
                        <small style="color: #ffd93d;">+{{ task.egg_reward }} Egg</small>
                        {% endif %}
                    </div>
                    {% if task.id in completed_tasks %}
                    <div class="task-xp">Completed!</div>
                    {% else %}
                    <a href="{% url 'pokemon:claim_task_xp' task.id %}" class="btn btn-primary" style="padding: 8px 15px; font-size: 0.9rem;">Claim +{{ task.xp_reward }} XP</a>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </div>'''

content = content.replace(old, new)

with open('pokemon/templates/pokemon/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
